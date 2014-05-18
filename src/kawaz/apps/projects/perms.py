from permission.logics import PermissionLogic


class ProjectPermissionLogic(PermissionLogic):
    """
    Permission logic which check object publish statement and return
    whether the user has a permission to see the object
    """

    def _has_join_perm(self, user_obj, perm, obj):
        if obj.pub_state == 'draft':
            # nobody can join to draft projects
            return False
        if not user_obj.is_authenticated():
            # anonymous user can't join to projects.
            return False
        if user_obj in obj.members.all():
            # member can not join to projects
            return False
        if user_obj.is_member:
            return True
        # Wille users cannot join to projects
        return False

    def _has_quit_perm(self, user_obj, perm, obj):
        # ToDo check if user is in children group
        if user_obj == obj.administrator:
            # administrator cannot quit the project
            return False
        if not user_obj.is_authenticated():
            # anonymous user cannot quit from projects.
            return False
        if user_obj not in obj.members.all():
            # non members cannot quit the project
            return False
        return True

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have a specified project permissions (of obj)
        """
        # anonymous use has no permissions
        if not user_obj.is_authenticated():
            return False
        # filter interest permissions
        if perm not in ('projects.add_project',
                        'projects.change_project',
                        'projects.delete_project',
                        'projects.join_project',
                        'projects.quit_project'):
            return False
        if obj is None:
            # seele, nerv, children have following permissions
            permissions = ('projects.add_project',
                           'projects.change_project',
                           'projects.delete_project',
                           'projects.join_project',
                           'projects.quit_project'
            )
            roles = ('seele', 'nerv', 'children')
            if perm in permissions and user_obj.role in roles:
                # seele, nerv, children have permissions of add, change, delete, join and quit project
                # generally
                return True
            return False
        # macros
        def author_required(user_obj, perm, obj):
            if user_obj.role not in ('seele', 'nerv', 'children'):
                return False
            return obj.administrator == user_obj
        # object permission
        permission_methods = {
            'projects.change_project': author_required,
            'projects.delete_project': author_required,
            'projects.join_project': self._has_join_perm,
            'projects.quit_project': self._has_quit_perm,
        }
        if perm in permission_methods:
            return permission_methods[perm](user_obj, perm, obj)
        return False
