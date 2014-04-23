import os
from django.conf import settings
from django.db import models
from django.db.models.base import ModelBase
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from thumbnailfield.fields import ThumbnailField

from kawaz.core.db.decorators import validate_on_save


class PersonaManager(BaseUserManager):
    """
    A custom user manager for the `Persona` model.

    This is required because `is_staff` and `is_superuser` fields are omitted
    from `Persona` model in database level.

    Instead of using these fields, `PersonaManager` use a `role` fields to
    distinguish the user and the superuser.
    When the user was created by `create_superuser` method, the `role` field of
    the user is specified to 'adam', otherwise to 'wille'.
    """
    def _create_user(self, username, email, password, role, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
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


class PersonaBase(ModelBase):
    """
    A metaclass of `Persona` model which remove inherited `is_staff` (from
    `AbstractUser`) and `is_superuser` (from `PermissionMixin`) fields.

    While `Persona` model have a `role` field and the value of `is_staff` or
    `is_superuser` are based on the `role` value, the database columns for
    these fields are unnecessary.

    Django use these values on its admin site but `is_staff` and `is_superuser`
    are defined as property attributes in the `Persona` class.
    Thus there should not be any exceptions with this field deletion (except
    for testing `is_staff` or `is_superuser` database values).

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
    A custom user model used in Kawaz

    This user model does not have `is_staff` and `is_superuser` database fields
    but properties.
    `is_staff` and `is_superuser` values are determined from the value of `role`
    field.
    """
    def _get_upload_path(self, filename):
        root = os.path.join('thumbnails', 'profiles', self.user.username)
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
    avatar = ThumbnailField(_('Avatar'), upload_to=_get_upload_path, blank=True,
                            patterns=settings.THUMBNAIL_SIZE_PATTERNS)
    gender = models.CharField(_('Gender'), max_length=10,
                              choices=GENDER_TYPES, default='unknown')
    role = models.CharField(_('Role'), max_length=10,
                            choices=ROLE_TYPES, default='wille',
                            help_text=_(
                                "The role this user belongs to. "
                                "A user will get permissions of the role thus "
                                "the user cannot change ones role for security "
                                "reason."
                            ))

    objects = PersonaManager()

    @property
    def is_staff(self):
        return self.role in ('adam', 'seele', 'nerv')

    @property
    def is_superuser(self):
        return self.role in ('adam',)

    class Meta:
        ordering = ('username',)
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')
        permissions = (
            ('view_persona', 'Can view the persona'),
            ('activate_persona', 'Can activate/deactivate the persona'),
            ('assign_role_persona', 'Can assign the role to the persona'),
        )

    def clean_fields(self, exclude=None, **kwargs):
        # automatically assign the nickname before field validation
        if not self.nickname:
            self.nickname = self.username
        super().clean_fields(exclude=exclude, **kwargs)

from permission import add_permission_logic
from .perms import PersonaPermissionLogic
add_permission_logic(Persona, PersonaPermissionLogic())
