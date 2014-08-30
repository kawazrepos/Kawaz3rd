import os
from django.conf import settings
from django.db import models
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from thumbnailfield.fields import ThumbnailField
from kawaz.core.publishments.models import PUB_STATES
from kawaz.core.publishments.models import PublishmentManagerMixin


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
        指定されたユーザーが閲覧可能なプロジェクトのうち、活動中のもののみ
        を含むクエリを返す
        """
        qs = self.published(user)
        return qs.filter(status='active')

    def archived(self, user):
        """
        指定されたユーザーがー閲覧可能なプロジェクトのうち
        アーカイブ化されたプロジェクトのクエリを返す
        以下のようなプロジェクトがアーカイブである

        状態がpaused, eternaled, doneのいずれかである
        状態がplanningかつ、created_atから90日以上経過している
        """
        import datetime
        from django.utils import timezone
        from django.db.models import Q
        now = timezone.now()
        three_months_ago = now - datetime.timedelta(days=3 * 30)
        status_q = Q(status__in=['paused', 'eternal', 'done'])
        planning_q = Q(status='planning')
        old_q = Q(created_at__lte=three_months_ago)
        return self.published(user).filter(status_q | (planning_q & old_q))

    def recently_planned(self, user):
        """
        指定されたユーザーがー閲覧可能なプロジェクトのうち
        最近企画されたプロジェクトのクエリを返す
        状態がplanningかつ、created_atが90日未満である
        """
        import datetime
        from django.utils import timezone
        now = timezone.now()
        past_day = now - datetime.timedelta(days=3 * 30)
        return self.published(user).filter(status='planning', created_at__gt=past_day)


# TODO: 所有権限の委託を可能にする
class Project(models.Model):
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
        ("paused",   _("Suspended")),
        ("eternal",  _("Eternaled")),
        ("done",     _("Released")),
    )

    # 必須フィールド
    pub_state = models.CharField(_("Publish status"),
                                 max_length=10, choices=PUB_STATES,
                                 default="public")
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
    body = models.TextField(_('Description'))

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

    tracker = models.URLField(_('Tracker URL'), blank=True, default='',
                              help_text='Kawaz RedmineのプロジェクトURLを入力してください')
    repository = models.URLField(_('Repository URL'), blank=True, default='',
                                 help_text='Kawaz GitLab, GitHubなどのプロジェクトURLを入力してください')

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

    def join(self, user, save=True):
        """
        指定されたユーザーを参加させる

        ユーザーに参加権限がない場合は `PermissionDenied` を投げる
        """
        if not user.has_perm('projects.join_project', self):
            raise PermissionDenied
        self.members.add(user)
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
from kawaz.core.personas.perms import KawazAuthorPermissionLogic
from permission.logics import CollaboratorsPermissionLogic
from kawaz.core.publishments.perms import PublishmentPermissionLogic
from .perms import ProjectPermissionLogic

add_permission_logic(Project, KawazAuthorPermissionLogic(
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
