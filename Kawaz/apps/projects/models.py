# -*- coding: utf-8 -*-
import os
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

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
        path = 'storage/projects/%s' % self.slug
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

    THUMBNAIL_SIZE_PATTERNS = {
        'huge':     (288, 288, False),
        'large':    (96, 96, False),
        'middle':   (48, 48, False),
        'small':    (24, 24, False),
    }
    # Required
    pub_state       = models.CharField(_('Publish state'), choices=PUB_STATES, max_length=10, default='public')
    status          = models.CharField(_("Status"), default="planning", max_length=15, choices=STATUS)
    title           = models.CharField(_('Title'), max_length=127, unique=True)
    slug            = models.SlugField(_('Project ID'), unique=True, max_length=63,
                                       help_text=_("This ID will be used for its URL. You can't modify it later. You can use only alphabetical characters, _ or -."))
    #body            = MarkItUpField(_('Description'), default_markup_type='markdown')
    # Omittable
    #icon            = ImageField(_('Thumbnail'), upload_to=_get_upload_path, blank=True, thumbnail_size_patterns=THUMBNAIL_SIZE_PATTERNS)
    category        = models.ForeignKey(Category, verbose_name=_('Category'), null=True, blank=True, related_name='projects',
                                        help_text="If a category you would like to use is not exist, please contact your administrator.")
    # Uneditable
    author          = models.ForeignKey(User, verbose_name=_('Organizer'), related_name="projects_owned", editable=False)
    updated_by      = models.ForeignKey(User, verbose_name=_('Last modifier'), related_name="projects_updated", editable=False)
    members         = models.ManyToManyField(User, verbose_name=_('Members'), related_name="projects_joined", editable=False)
    group           = models.ForeignKey(Group, verbose_name=_('Group'), unique=True, editable=False)
    created_at      = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at      = models.DateTimeField(_('Updated at'), auto_now=True)

    class Meta:
        ordering            = ('status', '-updated_at', 'title')
        verbose_name        = _('Project')
        verbose_name_plural = _('Projects')

    def __str__(self):
        return self.title

    def clean(self):
        if self.pk is None:
            group = Group.objects.get_or_create(name=u"project_%s" % self.slug)[0]
            self.group = group
        super(Project, self).clean()

    def save(self, *args, **kwargs):
        return super(Project, self).save(*args, **kwargs)

    def join_member(self, user, save=True):
        '''Add user to the project'''
        self.members.add(user)
        user.groups.add(self.group)
        if save:
            self.save(action='join')

    def quit_member(self, user, save=True):
        '''Remove user from the project'''
        if user == self.author:
            raise AttributeError("Author doesn't allow to quit the project")
        self.members.remove(user)
        user.groups.remove(self.group)
        if save:
            self.save(action='quit')