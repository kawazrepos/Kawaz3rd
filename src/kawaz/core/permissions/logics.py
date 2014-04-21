from permission.logics import AuthorPermissionLogic
from permission.utils.permissions import get_perm_codename

class RolePermissionLogic(AuthorPermissionLogic):
    """
    Permission logic class for role based permission system
    It is checked by user_obj.role
    """

    role_names = []

    def __init__(self,
                 any_permission=None,
                 change_permission=None,
                 delete_permission=None):
        """
        Constructor

        Parameters
        ----------
        any_permission : boolean
            True for give any permission of the specified object to the author
            Default value will be taken from
            ``PERMISSION_DEFAULT_APL_ANY_PERMISSION`` in
            settings.
        change_permission : boolean
            True for give change permission of the specified object to the
            author.
            It will be ignored if :attr:`any_permission` is True.
            Default value will be taken from
            ``PERMISSION_DEFAULT_APL_CHANGE_PERMISSION`` in
            settings.
        delete_permission : boolean
            True for give delete permission of the specified object to the
            author.
            It will be ignored if :attr:`any_permission` is True.
            Default value will be taken from
            ``PERMISSION_DEFAULT_APL_DELETE_PERMISSION`` in
            settings.
        """
        super().__init__(
            field_name=None,
            any_permission=any_permission,
            change_permission=change_permission,
            delete_permission=delete_permission
        )

    def has_perm(self, user_obj, perm, obj=None):
        codename = get_perm_codename(perm)
        if obj is None:
            return False
        elif user_obj.is_active:
            if user_obj:
                role = getattr(user_obj, 'role', None)
            if role and role in self.role_names:
                if self.any_permission:
                    # have any kind of permissions to the obj
                    return True
                if (self.change_permission and
                    codename.startswith('change_')):
                    return True
                if (self.delete_permission and
                    codename.startswith('delete_')):
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
