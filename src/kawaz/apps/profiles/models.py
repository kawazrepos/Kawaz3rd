import os
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model

from markupfield.fields import MarkupField

User = get_user_model()

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


class Profile(models.Model):
    """
    It is the model which indicates profiles of each users
    """

    # Profiles don't have 'draft' status.
    # So PUB_STATES is defined redundantly.
    PUB_STATES = (
        ('public',      _("Public")),
        ('protected',   _("Internal")),
    )

    # Required
    pub_state = models.CharField(_("Publish status"), max_length=10, choices=PUB_STATES, default="public")
    # Non required
    birthday = models.DateField(_('Birth day'), null=True, blank=True)
    place = models.CharField(_('Address'), max_length=255, blank=True, help_text=_('Your address will not be shown by anonymous user.'))
    url = models.URLField(_("URL"), max_length=255, blank=True)
    remarks = MarkupField(_("Remarks"), default_markup_type='markdown')
    skills = models.ManyToManyField(Skill, verbose_name=_('Skills'), related_name='users', null=True, blank=True)
    # Uneditable
    user = models.OneToOneField(User, verbose_name=_('User'), related_name='profile', unique=True, primary_key=True, editable=False)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)


    class Meta:
        ordering            = ('user__nickname',)
        verbose_name        = _("Profile")
        verbose_name_plural = _("Profiles")
        permissions = (
            ('view_profile', 'Can view the profile'),
        )

    def __str__(self):
        return self.user.nickname

class Service(models.Model):

    def _get_upload_path(self, filename):
        return os.path.join('services', filename)

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

from permission.logics import AuthorPermissionLogic
from permission import add_permission_logic
from kawaz.core.permissions.logics import PubStatePermissionLogic

from kawaz.core.permissions.logics import NervPermissionLogic

add_permission_logic(Skill, NervPermissionLogic(
    any_permission=True
))
add_permission_logic(Service, NervPermissionLogic(
    any_permission=True
))
add_permission_logic(Account, AuthorPermissionLogic(
    field_name='user',
    any_permission=True
))
add_permission_logic(Profile, AuthorPermissionLogic(
    field_name='user',
    change_permission=True,
    delete_permission=False
))
add_permission_logic(Profile, PubStatePermissionLogic())
