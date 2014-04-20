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
                            choices=ROLE_TYPES, default='wille')

    # overwrite `is_staff` field with property to disable db based
    # `is_staff` strategy.
    @property
    def is_staff(self):
        return self.role in ('adam', 'seele', 'nerv')
    @is_staff.setter
    def is_staff(self, val):
        # this is required to mimic the db field
        pass

    # overwrite `is_superuser` field with property to disable db based
    # `is_superuser` strategy
    @property
    def is_superuser(self):
        return self.role in ('adam',)
    @is_superuser.setter
    def is_superuser(self, val):
        # this is required to mimic the db field
        pass

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


from permission.logics import PermissionLogic
class PersonaPermissionLogic(PermissionLogic):
    """
    Permission logics which check the user's role and return corresponding
    permission
    """
    def _has_add_perm(self, user_obj, perm, obj):
        # only staff user can add user manually (in admin page)
        return user_obj.role in ('seele', 'nerv',)

    def _has_view_perm(self, user_obj, perm, obj):
        # owner or staff user can see the user info
        if obj is None:
            return False
        return obj == user_obj or user_obj.role in ('seele', 'nerv',)

    def _has_change_perm(self, user_obj, perm, obj):
        # owner and seele can change the user info manually
        if obj is None:
            return False
        return obj == user_obj or user_obj.role in ('seele',)

    def _has_delete_perm(self, user_obj, perm, obj):
        # nobody can delete user info except superuser
        if obj is None:
            return False
        return False

    def _has_activate_perm(self, user_obj, perm, obj):
        # only staff user can activate/deactivate user manually
        if obj is None:
            return False
        return user_obj.role in ('seele', 'nerv',)

    def _has_assign_role_perm(self, user_obj, perm, obj):
        # admin user can change user's role
        if obj is None:
            return False
        return user_obj.role in ('seele',)

    def has_perm(self, user_obj, perm, obj=None):
        permission_methods = {
            'personas.add_persona': self._has_add_perm,
            'personas.view_persona': self._has_view_perm,
            'personas.change_persona': self._has_change_perm,
            'personas.delete_persona': self._has_delete_perm,
            'personas.activate_persona': self._has_activate_perm,
            'personas.assign_role_persona': self._has_assign_role_perm,
        }
        if perm in permission_methods:
            return permission_methods[perm](user_obj, perm, obj)
        return False

from permission import add_permission_logic
add_permission_logic(Persona, PersonaPermissionLogic())
