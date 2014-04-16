import os
from django.db import models
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.db.models.signals import post_save
from django.dispatch import receiver

from thumbnailfield.fields import ThumbnailField
from markupfield.fields import MarkupField

class Category(models.Model):
    """
    This model indicates category of each projects
    """
    label = models.CharField(_('Name'), max_length=32, unique=True)
    parent = models.ForeignKey('self', verbose_name=_('Parent category'), null=True, blank=True, related_name='children')

    class Meta:
        ordering = ('label',)
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.label

class Project(models.Model):
    """The Project model"""
    def _get_upload_path(self, filename):
        path = 'thumbnails/projects/%s' % self.slug
        return os.path.join(path, filename)

    PUB_STATES = (
        ('public',      _("Public")),
        ('protected',   _("Internal")),
        ('draft',       _("Draft")),
    )
    STATUS = (
        ("planning",    _("Planning")),
        ("active",      _("Active")),
        ("eternal",     _("Eternaled")),
        ("done",        _("Released")),
    )

    # Required
    pub_state = models.CharField(_('Publish status'), choices=PUB_STATES, max_length=10, default='public')
    status = models.CharField(_("Status"), default="planning", max_length=15, choices=STATUS)
    title = models.CharField(_('Title'), max_length=127, unique=True)
    slug = models.SlugField(_('Project ID'), unique=True, max_length=63,
                            help_text=_("This ID will be used for its URL. You can't modify it later. You can use only alphabetical characters, _ or -."))
    body = MarkupField(_('Description'), default_markup_type='markdown')
    administrator = models.ForeignKey(User, verbose_name=_('Organizer'), related_name="projects_owned")
    # Omittable
    icon = ThumbnailField(_('Thumbnail'), upload_to=_get_upload_path, blank=True, patterns=settings.THUMBNAIL_SIZE_PATTERNS)
    category = models.ForeignKey(Category, verbose_name=_('Category'), null=True, blank=True, related_name='projects', help_text="If a category you would like to use is not exist, please contact your administrator.")
    # Uneditable
    members = models.ManyToManyField(User, verbose_name=_('Members'), related_name="projects_joined", editable=False)
    group = models.ForeignKey(Group, verbose_name=_('Group'), unique=True, editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

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
            group = Group.objects.get_or_create(name="project_%s" % self.slug)[0]
            self.group = group
        return super(Project, self).save(*args, **kwargs)

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

@receiver(post_save, sender=Project)
def join_administrator(**kwargs):
    created = kwargs.get('created')
    instance = kwargs.get('instance')
    if created and instance.pub_state != 'draft':
        instance.join(instance.administrator)

from permission.logics import PermissionLogic

class ProjectPermissionLogic(PermissionLogic):
    """
    Permission logic which check object publish statement and return
    whether the user has a permission to see the object
    """
    def _has_view_perm(self, user_obj, perm, obj):
        if obj.pub_state == 'protected':
            # only authorized user can show protected project
            return user_obj.is_authenticated()
        if obj.pub_state == 'draft':
            # only administrator user can show draft project
            return user_obj == obj.administrator
        # public
        return True

    def _has_join_perm(self, user_obj, perm, obj):
        if obj.pub_state == 'draft':
            # nobody can join to draft projects
            return False
        if not user_obj.is_authenticated():
            # anonymous user can't join to projects.
            return False
        if user_obj in obj.members.all():
            # member can not join to projects
            return False
        return True

    def _has_quit_perm(self, user_obj, perm, obj):
        # ToDo check if user is in children group
        if user_obj == obj.administrator:
            # administrator cannot quit the event
            return False
        if not user_obj.is_authenticated():
            # anonymous user cannot quit from projects.
            return False
        if user_obj not in obj.members.all():
            # non members cannot quit the event
            return False
        return True

    def has_perm(self, user_obj, perm, obj=None):
        # treat only object permission
        if obj is None:
            return False
        permission_methods = {
            'projects.view_project': self._has_view_perm,
            'projects.join_project': self._has_join_perm,
            'projects.quit_project': self._has_quit_perm,
        }
        if perm in permission_methods:
            return permission_methods[perm](user_obj, perm, obj)
        return False

from permission import add_permission_logic
from permission.logics import AuthorPermissionLogic
from permission.logics import CollaboratorsPermissionLogic

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
