import os
from django.conf import settings
from django.db import models
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.contrib.auth.models import Group
from thumbnailfield.fields import ThumbnailField
from markupfield.fields import MarkupField
from kawaz.core.publishment.models import AbstractPublishmentModel
from kawaz.core.publishment.models import PublishmentManagerMixin


class Category(models.Model):
    """
    プロジェクトが所属するカテゴリモデル

    スタッフが作成し、メンバーがプロジェクト作成・編集時に利用する
    """
    label = models.CharField(_('Name'), max_length=32, unique=True)
    parent = models.ForeignKey('self', verbose_name=_('Parent category'),
                               null=True, blank=True, related_name='children')

    class Meta:
        ordering = ('label',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.label


class ProjectManager(models.Manager, PublishmentManagerMixin):
    author_field_name = 'administrator'

    def active(self, user):
        """
        指定されたユーザーが閲覧可能なプロジェクトのうち、アクティブなもののみ
        を含むクエリを返す
        """
        qs = self.published(user)
        return qs.exclude(status='eternal')


# TODO: 所有権限の委託を可能にする
class Project(AbstractPublishmentModel):
    """
    現在進行形で作成しているプロジェクトを示すモデル

    メンバーであれば自由に作成可能で所有者および参加者が編集権限を持つ
    また削除権限は所有者のみが持ち、所有権限の委託は未だ作成されていない。
    """
    def _get_upload_path(self, filename):
        basedir = os.path.join('thumbnails', 'projects', self.slug)
        return os.path.join(basedir, filename)

    STATUS = (
        ("planning", _("Planning")),
        ("active",   _("Active")),
        ("eternal",  _("Eternaled")),
        ("done",     _("Released")),
    )

    # 必須フィールド
    status = models.CharField(_("Status"), default="planning",
                              max_length=15, choices=STATUS)
    title = models.CharField(_('Title'), max_length=127, unique=True)
    slug = models.SlugField(_('Project slug'), unique=True, max_length=63,
                            help_text=_("It will be used on the url of the "
                                        "project thus it only allow "
                                        "alphabetical or numeric "
                                        "characters, underbar ('_'), and "
                                        "hyphen ('-'). "
                                        "Additionally this value cannot be "
                                        "modified for preventing the URL "
                                        "changes."))
    body = MarkupField(_('Description'), default_markup_type='markdown')

    # 省略可能フィールド
    icon = ThumbnailField(_('Thumbnail'), upload_to=_get_upload_path,
                          blank=True,
                          patterns=settings.THUMBNAIL_SIZE_PATTERNS)
    category = models.ForeignKey(Category, verbose_name=_('Category'),
                                 null=True, blank=True,
                                 related_name='projects',
                                 help_text=_("Contact us if you cannot find "
                                             "a category you need."))
    # 自動/API設定
    administrator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      verbose_name=_('Administrator'),
                                      related_name="projects_owned",
                                      editable=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     verbose_name=_('Members'),
                                     related_name="projects_joined",
                                     editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    # TODO: group 要素は 2nd では必要だった（databased object permission）が
    #       3rd では不要なため（logic based object permission）削る
    group = models.ForeignKey(Group, verbose_name=_('Group'),
                              unique=True, editable=False)

    objects = ProjectManager()

    class Meta:
        ordering = ('status', '-updated_at', 'title')
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        permissions = (
            ('join_project', 'Can join to the project'),
            ('quit_project', 'Can quit from the project'),
            ('view_project', 'Can view the project'),
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            group_name = "project_" + self.slug
            self.group = Group.objects.get_or_create(name=group_name)[0]
        return super().save(*args, **kwargs)

    def join(self, user, save=True):
        """
        指定されたユーザーを参加させる

        ユーザーに参加権限がない場合は `PermissionDenied` を投げる
        """
        if not user.has_perm('projects.join_project', self):
            raise PermissionDenied
        self.members.add(user)
        user.groups.add(self.group)
        if save:
            self.save()

    def quit(self, user, save=True):
        """
        指定されたユーザーを退会させる

        ユーザーに退会権限がない場合は `PermissionDenied` を投げる
        """
        if not user.has_perm('projects.quit_project', self):
            raise PermissionDenied
        self.members.remove(user)
        user.groups.remove(self.group)
        if save:
            self.save()

    # TODO: Persona.is_member と若干かぶるため名前を変えたほうが良い
    def is_member(self, user):
        """
        指定されたユーザーがこのプロジェクトに参加しているか否か
        """
        return user in self.members.all()

    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ('projects_project_update', (), {
                'pk': self.pk
            })
        return ('projects_project_detail', (), {
            'slug': self.slug
        })


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Project)
def join_administrator(**kwargs):
    """
    プロジェクト作成時に自動的に管理者をプロジェクトに参加させるシグナル処理
    """
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created and instance.pub_state != 'draft':
        instance.join(instance.administrator)


from permission import add_permission_logic
from permission.logics import AuthorPermissionLogic
from permission.logics import CollaboratorsPermissionLogic
from kawaz.core.publishment.perms import PublishmentPermissionLogic
from .perms import ProjectPermissionLogic

add_permission_logic(Project, AuthorPermissionLogic(
    field_name='administrator',
    change_permission=True,
    delete_permission=True
))
add_permission_logic(Project, CollaboratorsPermissionLogic(
    field_name='members',
    change_permission=True,
    delete_permission=False
))
add_permission_logic(Project, ProjectPermissionLogic())
add_permission_logic(Project, PublishmentPermissionLogic(
    author_field_name='administrator'
))
