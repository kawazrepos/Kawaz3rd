import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.exceptions import ValidationError

from thumbnailfield.fields import ThumbnailField

from kawaz.core.db.decorators import validate_on_save

@validate_on_save
class Persona(AbstractUser):

    def _get_upload_path(self, filename):
        return os.path.join('thumbnails', 'profiles', self.user.username, filename)

    GENDER_TYPES = (
        ('man',   _("Man")),
        ('woman', _("Woman")),
        ('unknown', _("Unknown"))
    )

    ROLE_TYPES = (
        ('adam', _('Adam')), # roles for the god
        ('seele', _('Seele')), # roles for admin users
        ('nerv', _('Nerv')), # roles for staff users
        ('children', _('Children')), # roles for general users
        ('wille', _('Wille')), # roles for external users
    )

    nickname = models.CharField(_('Nickname'), max_length=30)
    quotes = models.CharField(_('Mood message'), max_length=127, blank=True, null=True)
    avatar = ThumbnailField(_('Avatar') , upload_to=_get_upload_path, blank=True, patterns=settings.THUMBNAIL_SIZE_PATTERNS, null=True)
    gender = models.CharField(_('Gender'), max_length=10, choices=GENDER_TYPES, default='unknown')
    role = models.CharField(_('Role'), max_length=10, choices=ROLE_TYPES, default='children')

    class Meta:
        ordering = ('username',)
        verbose_name = _('Persona')
        verbose_name_plural = _('Personas')
        permissions = (
            ('change_persona_role', 'Can change the persona role'),
            ('change_persona_is_active', 'Can change is_active'),
            ('view_persona', 'Can view the persona info'),
        )

    def clean(self):
        if self.is_staff and not (self.role == 'seele' or self.role == 'nerv'):
            raise ValidationError('staff user must be seele of Nerv role')
        elif self.is_superuser and not self.role == 'seele':
            raise ValidationError('superuser must be Seele role')
        return super().clean()

    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.username
        if self.role == 'seele':
            self.is_staff = True
            self.is_superuser = True
        elif self.role == 'nerv':
            self.is_staff = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

from permission.logics import PermissionLogic

class PersonaPermissionLogic(PermissionLogic):
    """
    Permission logic which check object publish statement and return
    whether the user has a permission to see the object
    """
    def _has_view_perm(self, user_obj, perm, obj):
        # owner or staff user can show user info
        return obj == user_obj or user_obj.is_staff()

    def _has_change_perm(self, user_obj, perm, obj):
        # owner can change user info
        return obj == user_obj

    def _has_delete_perm(self, user_obj, perm, obj):
        # nobody can delete user info
        return False

    def _has_change_role_perm(self, user_obj, perm, obj):
        # admin user can change user's role
        return user_obj.is_superuser()

    def _has_add_perm(self, user_obj, perm, obj):
        # staff user can add user
        return user_obj.is_staff()

    def _has_change_is_active_perm(self, user_obj, perm, obj):
        # user can't activate own account
        return user_obj.is_staff()

    def has_perm(self, user_obj, perm, obj=None):
        permission_methods = {
            'personas.view_persona': self._has_view_perm,
            'personas.add_persona': self._has_add_perm,
            'personas.change_persona': self._has_change_perm,
            'personas.delete_persona': self._has_delete_perm,
            'personas.change_persona_role': self._has_add_perm,
            'personas.change_is_active': self._has_change_is_active_perm,
        }
        if perm in permission_methods:
            return permission_methods[perm](user_obj, perm, obj)
        return False

from permission import add_permission_logic

add_permission_logic(Persona, PersonaPermissionLogic())