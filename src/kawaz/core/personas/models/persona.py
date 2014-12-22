import re
import os

from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from thumbnailfield.fields import ThumbnailField

from kawaz.core.db.decorators import validate_on_save


# kawaz.core.personas
# 使用可能なユーザー名の正規表現
VALID_USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9\^\-\_]+$")
# 使用不可なユーザー名（URLルールなどにより）
INVALID_USERNAMES = (
    'my',
)


class PersonaManager(BaseUserManager):
    """
    Persona用カスタムマネージャ

    PersonaモデルはDjangoがデフォルトで利用する `is_staff` や `is_superuser` を
    DBレベルで廃止しているため、このカスタムが必要

    PersonaManagerでは`role`によりユーザーとスーパーユーザを区別しているため
    `create_superuser`で作成されたユーザーは`role`が`'adam'`になり、その他の
    場合は`'wille'`となる。
    """
    def _create_user(self, username, email, password, role, **extra_fields):
        """
        与えられたユーザー名、メールアドレスおよびパスワードと役職から新しい
        ユーザーインスタンスをDB上に作成する
        """
        now = timezone.now()
        if not username:
            raise ValueError(_('The `username` attribute is required'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_active=True, last_login=now, role=role,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, 'wille',
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, 'adam',
                                 **extra_fields)


class ActivePersonaManager(PersonaManager):
    """
    アクティブユーザーのみを取り出すManager
    """
    use_for_related_fields = True

    def get_queryset(self):
        # 常に無効なユーザーは含まない
        return super().get_query_set().filter(is_active=True)


class PersonaBase(ModelBase):
    """
    `AbstractUser`から継承されたために自動作成される`is_staff`や`is_superuser`
    フィールドを強制的に削除するためのメタクラス

    `Persona`モデルは`role`フィールドを持ち、その値により`is_staff`や
    `is_superuser`の値を決定するためDB上にこれらの値を保持する必要性がない。
    """
    def __init__(cls, class_name, bases, namespace):
        disused_field_names = ('is_staff', 'is_superuser')
        disused_fields = [f for f in cls._meta.fields if f.name in
                          disused_field_names]
        for field in disused_fields:
            # remove disused fields from `local_fields` and `fields`
            cls._meta.local_fields.remove(field)
            cls._meta.fields.remove(field)
        # clear cache
        del cls._meta._field_cache
        del cls._meta._field_name_cache


@validate_on_save
class Persona(AbstractUser, metaclass=PersonaBase):
    """
    Kawazで利用する認証用カスタムユーザーモデル

    このユーザーモデルはDjangoデフォルトのモデルと異なり`is_staff`と
    `is_superuser`の値をDB上に保持しない。代わりにこれらの値は`role`の値から
    自動的に決定され、プロパティとして提供される
    """
    def _get_upload_path(self, filename):
        root = os.path.join('personas', 'avatars', self.username)
        return os.path.join(root, filename)

    GENDER_TYPES = (
        ('man',   _("Man")),
        ('woman', _("Woman")),
        ('unknown', _("Unknown"))
    )

    ROLE_TYPES = (
        ('adam', _('Adam')),            # superusers
        ('seele', _('Seele')),          # admin
        ('nerv', _('Nerv')),            # staff
        ('children', _('Children')),    # Kawaz members
        ('wille', _('Wille')),          # external users
    )

    nickname = models.CharField(_('Nickname'), max_length=30)
    quotes = models.CharField(_('Mood message'), max_length=127, blank=True)
    avatar = ThumbnailField(_('Avatar'),
                            upload_to=_get_upload_path, blank=True,
                            patterns=settings.THUMBNAIL_SIZE_PATTERNS)
    gender = models.CharField(_('Gender'), max_length=10,
                              choices=GENDER_TYPES, default='unknown')
    role = models.CharField(_('Role'), max_length=10,
                            choices=ROLE_TYPES, default='wille',
                            help_text=_(
                                "The role this user belongs to. "
                                "A user will get permissions of the role thus "
                                "the user cannot change ones role for "
                                "security reason."))

    objects = PersonaManager()
    actives = ActivePersonaManager()

    class Meta:
        ordering = ('username',)
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')
        permissions = (
            ('activate_persona', 'Can activate/deactivate the persona'),
            ('assign_role_persona', 'Can assign the role to the persona'),
        )

    @property
    def is_staff(self):
        return self.role in ('adam', 'seele', 'nerv')

    @property
    def is_superuser(self):
        return self.role in ('adam',)

    @property
    def is_member(self):
        return self.role in ('adam', 'seele', 'nerv', 'children')

    def get_default_avatar(self, size):
        """
        デフォルトアバターを返します
        """
        filename = 'persona_avatar_{}.png'.format(size)
        return os.path.join('/statics', 'img', 'defaults', filename)

    def get_avatar(self, size):
        """
        渡したサイズのアバターURLを返します
        未設定の場合や、見つからない場合はデフォルトアバターを返します
        """
        if self.avatar:
            try:
                return getattr(self.avatar, size).url
            except:
                return self.get_default_avatar(size)
        return self.get_default_avatar(size)

    get_small_avatar = lambda self: self.get_avatar('small')
    get_middle_avatar = lambda self: self.get_avatar('middle')
    get_large_avatar = lambda self: self.get_avatar('large')
    get_huge_avatar = lambda self: self.get_avatar('huge')

    def clean_fields(self, exclude=None, **kwargs):
        # 使用不可な文字列が指定されていた場合はエラー
        # Note:
        #   AbstractUser では RegexValidator('^[\\w.@+-]+$')
        #   でチェックしているが Kawaz の仕様的に . @ + は使用できると不味い
        #   ので追加でチェックしている
        if not VALID_USERNAME_PATTERN.match(self.username):
            raise ValidationError(_(
                "The username '%(username)s' contains invalid characters. "
                "Letters, digits, and - are the only characters available."
            ) % {'username': self.username})
        # 使用不可のユーザー名が指定されていた場合はエラー
        if self.username in INVALID_USERNAMES:
            raise ValidationError(_(
                "The username '%(username)s' is reserved. "
                "Please chose a different username."
            ) % {'username': self.username})
        # ニックネームが指定されていない場合は自動的にユーザー名を当てはめる
        if not self.nickname:
            self.nickname = self.username
        super().clean_fields(exclude=exclude, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ('personas_persona_detail', (), {
            'slug': self.username
        })
# username に対し独自のValidationをかけているためデフォルトのhelp_textと
# 実情があっていないため、強制的に書き換える
Persona._meta.get_field('username').help_text = _(
    'Required. 30 characters or fewer. Letters, digits and /-/_ only.'
)

from permission import add_permission_logic
from ..perms import PersonaPermissionLogic
add_permission_logic(Persona, PersonaPermissionLogic())

from ..activities.persona import PersonaActivityMediator
from activities.registry import registry
registry.register(Persona, PersonaActivityMediator())
