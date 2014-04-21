from django.conf import settings
from permission.logics import PermissionLogic
from permission.utils.permissions import get_perm_codename

class RolePermissionLogic(PermissionLogic):
    """
    Permission logic class for role based permission system
    It is checked by user_obj.role
    """

    role_names = []

    def __init__(self,
                 any_permission=False,
                 add_permission=False,
                 change_permission=False,
                 delete_permission=False):
        """
        Constructor

        Parameters
        ----------
        any_permission : boolean
        add_permission : boolean
        change_permission : boolean
        delete_permission : boolean
        """
        self.any_permission = any_permission
        self.add_permission = add_permission
        self.change_permission = change_permission
        self.delete_permission = delete_permission

    def has_perm(self, user_obj, perm, obj=None):
        add_name = self.get_full_permission_string('add')
        change_name = self.get_full_permission_string('change')
        delete_name = self.get_full_permission_string('delete')
        if not user_obj.is_active:
            return False
        if user_obj:
            role = getattr(user_obj, 'role', None)
        if obj is None:
            if (self.any_permission or self.add_permission) and perm == add_name:
                if role in self.role_names:
                    return True
            return False
        else:
            if role and role in self.role_names:
                if self.any_permission:
                    # have any kind of permissions to the obj
                    return True
                if self.change_permission and perm == change_name:
                    return True
                if self.delete_permission and perm == delete_name:
                    return True
        return False


class ChildrenPermissionLogic(RolePermissionLogic):
    role_names = ['seele', 'nerv', 'children', 'adam']


class NervPermissionLogic(RolePermissionLogic):
    role_names = ['adam', 'seele', 'nerv',]


class SeelePermissionLogic(RolePermissionLogic):
    role_names = ['adam', 'seele',]


class AdamPermissionLogic(RolePermissionLogic):
    role_names = ['adam',]
