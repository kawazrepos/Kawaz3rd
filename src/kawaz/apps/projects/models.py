import os
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from thumbnailfield.fields import ThumbnailField
from markupfield.fields import MarkupField

from kawaz.core.permissions.logics import PUB_STATES


class Category(models.Model):
    """
    This model indicates category of each projects
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


class ProjectManager(models.Manager):
    '''ObjectManager for Project model'''

    def active(self, user):
        qs = self.published(user)
        qs = qs.exclude(status='eternal')
        return qs.distinct()

    def published(self, user):
        q = Q(pub_state='public')
        if user.is_authenticated() and not user.role in ['wille',]:
            q |= Q(pub_state='protected')
        return self.filter(q).distinct()

    def draft(self, user):
        if user and user.is_authenticated():
            return self.filter(administrator=user, pub_state='draft')
        return self.none()


class Project(models.Model):
    """The Project model"""
    def _get_upload_path(self, filename):
        path = 'thumbnails/projects/%s' % self.slug
        return os.path.join(path, filename)

    STATUS = (
        ("planning",    _("Planning")),
        ("active",      _("Active")),
        ("eternal",     _("Eternaled")),
        ("done",        _("Released")),
    )

    # Required
    pub_state = models.CharField(_('Publish status'), choices=PUB_STATES,
                                 max_length=10, default='public')
    status = models.CharField(_("Status"), default="planning",
                              max_length=15, choices=STATUS)
    title = models.CharField(_('Title'), max_length=127, unique=True)
    slug = models.SlugField(_('Project ID'), unique=True, max_length=63,
                            help_text=_("This ID will be used for its URL. "
                                        "You can't modify it later. "
                                        "You can use only alphabetical "
                                        "characters or some delimiters ('_' or "
                                        "'-')."))
    body = MarkupField(_('Description'), default_markup_type='markdown')
    # Omittable
    icon = ThumbnailField(_('Thumbnail'), upload_to=_get_upload_path,
                          blank=True, 
                          patterns=settings.THUMBNAIL_SIZE_PATTERNS)
    category = models.ForeignKey(Category, verbose_name=_('Category'),
                                 null=True, blank=True,
                                 related_name='projects',
                                 help_text=_("If a category you would like to "
                                             "use is not exist, please contact "
                                             "your administrator."))
    # Uneditable
    administrator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      verbose_name=_('Administrator'),
                                      related_name="projects_owned",
                                      editable=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     verbose_name=_('Members'),
                                     related_name="projects_joined",
                                     editable=False)
    group = models.ForeignKey(Group, verbose_name=_('Group'),
                              unique=True, editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

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
        '''Add user to the project'''
        if not user.has_perm('projects.join_project', self):
            raise PermissionDenied
        self.members.add(user)
        user.groups.add(self.group)
        if save:
            self.save()

    def quit(self, user, save=True):
        '''Remove user from the project'''
        if not user.has_perm('projects.quit_project', self):
            raise PermissionDenied
        self.members.remove(user)
        user.groups.remove(self.group)
        if save:
            self.save()

    def is_member(self, user):
        '''Check passed user is whether member or not'''
        return user in self.members.all()

    @models.permalink
    def get_absolute_url(self):
        if self.pub_state == 'draft':
            return ('projects_project_update', (), {
                'pk' : self.pk
            })
        return ('projects_project_detail', (), {
            'slug' : self.slug
        })


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Project)
def join_administrator(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created and instance.pub_state != 'draft':
        instance.join(instance.administrator)


from permission import add_permission_logic
from permission.logics import AuthorPermissionLogic
from permission.logics import CollaboratorsPermissionLogic
from kawaz.core.permissions.logics import PubStatePermissionLogic
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
add_permission_logic(Project, PubStatePermissionLogic(
    author_field_name='administrator'
))
