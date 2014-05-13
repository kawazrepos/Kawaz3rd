from permission.logics import PermissionLogic

class StarPermissionLogic(PermissionLogic):
    """
    Permission logic which check object publish statement and return
    whether the user has a permission to see the object
    """

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have a specified star permissions (of obj)
        """
        # anonymous use has no permissions
        if not user_obj.is_authenticated():
            return False
        # filter interest permissions
        if perm not in ('stars.add_star',
                        'stars.change_star',
                        'stars.delete_star'):
            return False
        if perm == 'stars.change_star':
            # nobody can change stars
            return False
        if obj is None:
            # seele, nerv, children have following permissions
            permissions = ('stars.add_star',
                           'stars.delete_star',
            )
            roles = ('seele', 'nerv', 'children')
            if perm in permissions and user_obj.role in roles:
                # seele, nerv, children have permissions of add, change and delete star
                # generally
                return True
            return False
        # macros
        def author_required(user_obj, perm, obj):
            if user_obj.role not in ('seele', 'nerv', 'children'):
                return False
            return obj.author == user_obj
        # object permission
        permission_methods = {
            'stars.delete_star': author_required,
        }
        if perm in permission_methods:
            return permission_methods[perm](user_obj, perm, obj)
        return False