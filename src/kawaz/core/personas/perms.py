# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
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
        return obj == user_obj or user_obj.role in ('seele', 'nerv',)

    def _has_change_perm(self, user_obj, perm, obj):
        # owner and seele can change the user info manually
        return obj == user_obj or user_obj.role in ('seele', 'nerv')

    def _has_delete_perm(self, user_obj, perm, obj):
        # nobody can delete user info except superuser
        return False

    def _has_activate_perm(self, user_obj, perm, obj):
        # only staff user can activate/deactivate user manually
        return user_obj.role in ('seele', 'nerv',)

    def _has_assign_role_perm(self, user_obj, perm, obj):
        # admin user can change user's role
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

