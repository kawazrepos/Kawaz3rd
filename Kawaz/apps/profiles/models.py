# -*- coding: utf-8 -*-
import os
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from Kawaz.apps.markitupfield.models import MarkItUpField
from Kawaz.apps.imagefield.fields import ImageField

class Skill(models.Model):
    """It is the model which indicates what users can"""
    label = models.CharField(_('Label'), unique=True, max_length=32)
    description = models.CharField(_('Description'), max_length=128)
    order = models.IntegerField(_("Order"), default=0)

    def __unicode__(self):
        return self.label

    class Meta:
        ordering = ('order', 'pk',)
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

class ProfileManager(models.Manager):
    def active_users(self, request):
        qs = self.exclude(nickname=None).exclude(user__is_active=False)
        return qs

class Profile(models.Model):
    u"""
    It is the model which indicates profiles of each users

    このモデルはauth.Userのmoduleとして利用されます
    user.get_profile()で取得できます
    AbstractUserを利用しない理由として、以下の2点が挙げられます
    - 1. Kawaz 2ndのProfileモデルとの互換性
    - 2. 古いDjango向けに作られたプラグインとの互換性
    """

    def _get_upload_path(self, filename):
        path = u'storage/profiles/%s' % self.user.username
        return os.path.join(path, filename)

    SEX_TYPES = (
        ('man',   _("Man")),
        ('woman', _("Woman"))
    )
    THUMBNAIL_SIZE_PATTERNS = {
        'huge':     (288, 288, False),
        'large':    (96, 96, False),
        'middle':   (48, 48, False),
        'small':    (24, 24, False),
    }

    # Required
    nickname = models.CharField(_('Nickname'), max_length=30, unique=True, blank=False, null=True)
    # Non required
    mood = models.CharField(_('Mood message'), max_length=127, blank=True)
    #icon = ImageField(_('Avatar') , upload_to=_get_upload_path, blank=True, thumbnail_size_patterns=THUMBNAIL_SIZE_PATTERNS, null=True)
    sex  = models.CharField('Gender', max_length=10, choices=SEX_TYPES, blank=True)
    birthday = models.DateField(_('Birth day'), null=True, blank=True)
    place = models.CharField(_('Address'), max_length=255, blank=True, help_text=_('Your address will not be shown by anonymous user.'))
    url = models.URLField(_("URL"), max_length=255, blank=True)
    #remarks = MarkItUpField(_("Remarks"), default_markup_type='html', blank=True, null=True)
    skills = models.ManyToManyField(Skill, verbose_name=_('Skills'), related_name='users', null=True, blank=True)
    # Uneditable
    user = models.ForeignKey(User, verbose_name=_('User'), related_name='profile', unique=True, primary_key=True, editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    objects = ProfileManager()

    class Meta:
        ordering            = ('-user__last_login', 'nickname')
        verbose_name        = _("Profile")
        verbose_name_plural = _("Profiles")

    def __unicode__(self):
        if self.nickname:
            return self.nickname
        return _('Non Active User : %(username)s') % {'username' : self.user.username}

    def modify_object_permission(self, mediator, created):
        # Permission
        mediator.manager(self, self.user)
        if self.pub_state == 'public':
            mediator.viewer(self, None)
            mediator.viewer(self, 'anonymous')
        else:
            mediator.viewer(self, None)
            mediator.reject(self, 'anonymous')

    @models.permalink
    def get_absolute_url(self):
        return ("profiles-profile-detail", (), {'slug': self.user.username})

class Service(models.Model):

    def _get_upload_path(self, filename):
        return os.path.join(["storage/services", filename])

    label = models.CharField(_('Label'), max_length=64, unique=True)
    description = models.CharField(_('Description'), max_length=256)
    icon = models.ImageField(_('Icon'), upload_to=_get_upload_path)
    url_pattern = models.CharField(_('URL pattern'), max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

class Account(models.Model):
    user = models.ForeignKey(User, verbose_name=_('Profile'))
    service = models.ForeignKey(Service, verbose_name=_('Service'))
    username = models.CharField(_('Username'), max_length=64)

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    def __unicode__(self):
        return "%s (%s @ %s)" % (self.username, self.user.username, self.service.label)

    @property
    def url(self):
        return self.service.url_pattern % self.username
