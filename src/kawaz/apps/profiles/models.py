import os
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.conf import settings

from thumbnailfield.fields import ThumbnailField
from markupfield.fields import MarkupField

class Skill(models.Model):
    """It is the model which indicates what users can"""
    label = models.CharField(_('Label'), unique=True, max_length=32)
    description = models.CharField(_('Description'), max_length=128)
    order = models.IntegerField(_("Order"), default=0)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('order', 'pk',)
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

class ProfileManager(models.Manager):
    # ToDo Test me
    def active_users(self, request):
        qs = self.exclude(nickname=None).exclude(user__is_active=False)
        return qs

class Profile(models.Model):
    """
    It is the model which indicates profiles of each users
    """

    def _get_upload_path(self, filename):
        path = 'thumbnails/profiles/%s' % self.user.username
        return os.path.join(path, filename)

    GENDER_TYPES = (
        ('man',   _("Man")),
        ('woman', _("Woman"))
    )
    PUB_STATES = (
        ('public',      _("Public")),
        ('protected',   _("Internal")),
    )

    # Required
    pub_state = models.CharField(_("Publish status"), max_length=10, choices=PUB_STATES, default="public")
    nickname = models.CharField(_('Nickname'), max_length=30, unique=True, blank=False, null=True)
    # Non required
    mood = models.CharField(_('Mood message'), max_length=127, blank=True)
    avatar = ThumbnailField(_('Avatar') , upload_to=_get_upload_path, blank=True, patterns=settings.THUMBNAIL_SIZE_PATTERNS, null=True)
    gender  = models.CharField('Gender', max_length=10, choices=GENDER_TYPES, blank=True)
    birthday = models.DateField(_('Birth day'), null=True, blank=True)
    place = models.CharField(_('Address'), max_length=255, blank=True, help_text=_('Your address will not be shown by anonymous user.'))
    url = models.URLField(_("URL"), max_length=255, blank=True)
    remarks = MarkupField(_("Remarks"), default_markup_type='markdown')
    skills = models.ManyToManyField(Skill, verbose_name=_('Skills'), related_name='users', null=True, blank=True)
    # Uneditable
    user = models.OneToOneField(User, verbose_name=_('User'), related_name='profile', unique=True, primary_key=True, editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)

    objects = ProfileManager()

    class Meta:
        ordering            = ('nickname',)
        verbose_name        = _("Profile")
        verbose_name_plural = _("Profiles")
        permissions = (
            ('view_profile', 'Can view the profile'),
        )

    def __str__(self):
        if self.nickname:
            return self.nickname
        return _('Non Active User : %(username)s') % {'username' : self.user.username}

from permission.logics import PermissionLogic
class ProfilePermissionLogic(PermissionLogic):
    """
    Permission logic which check object publish statement and return
    whether the user has a permission to see the object
    """
    def _has_view_perm(self, user_obj, perm, obj):
        if obj.pub_state == 'protected':
            return user_obj.is_authenticated()
        # public
        return True

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check `obj.pub_state` and if user is authenticated
        """
        # treat only object permission
        if obj is None:
            return False
        permission_methods = {
            'profiles.view_profile': self._has_view_perm,
        }
        if perm in permission_methods:
            return permission_methods[perm](user_obj, perm, obj)
        return False

from permission.logics import AuthorPermissionLogic
from permission import add_permission_logic

add_permission_logic(Profile, ProfilePermissionLogic())
add_permission_logic(Profile, AuthorPermissionLogic(
    field_name='user',
    change_permission=True,
    delete_permission=False
))

class Service(models.Model):

    def _get_upload_path(self, filename):
        return os.path.join(["services", filename])

    label = models.CharField(_('Label'), max_length=64, unique=True)
    icon = models.ImageField(_('Icon'), upload_to=_get_upload_path)
    url_pattern = models.CharField(_('URL pattern'), max_length=256, null=True, blank=True)

    def __str__(self):
        return self.label

    class Meta:
        ordering = ('pk',)
        verbose_name = _('Service')
        verbose_name_plural = _('Services')

class Account(models.Model):
    user = models.ForeignKey(User, verbose_name=_('Profile'))
    service = models.ForeignKey(Service, verbose_name=_('Service'))
    username = models.CharField(_('Username'), max_length=64)

    class Meta:
        verbose_name = _('Account')
        verbose_name_plural = _('Accounts')

    def __str__(self):
        return "%s (%s @ %s)" % (self.username, self.user.username, self.service.label)

    @property
    def url(self):
        return self.service.url_pattern % self.username
