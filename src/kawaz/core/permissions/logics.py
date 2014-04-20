from permission.logics import AuthorPermissionLogic
from permission.utils.permissions import get_perm_codename

class RolePermissionLogic(AuthorPermissionLogic):
    """
    Permission logic class for role based permission system
    It is checked by Persona.role
    """

    def has_perm(self, user_obj, perm, obj=None):
        codename = get_perm_codename(perm)
        if obj is None:
            return False
        elif user_obj.is_active:
            author = getattr(obj, self.field_name, None)
            role = getattr(author, 'role', None)
            if author and role and author.role in self.role_names:
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
    role_names = ['seele', 'nerv',]

class SeelePermissionLogic(RolePermissionLogic):
    role_names = ['seele',]