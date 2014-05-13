from permission.logics import PermissionLogic

class AnnouncementPermissionLogic(PermissionLogic):
    """
    Permission logic which check object publish statement and return
    whether the user has a permission to see the object
    """

    # announcementは、draftの扱いが異なるため、PubStatePermissionLogicを使用していない
    def _has_view_perm(self, user_obj, perm, obj):
        if obj.pub_state == 'protected':
            # only authorized user can show protected announcement
            return user_obj and user_obj.is_authenticated() and user_obj.role != 'wille'
        if obj.pub_state == 'draft':
            # only staff user can show draft announcement
            return user_obj.is_staff
        # public
        return True

    def has_perm(self, user_obj, perm, obj=None):
        allowed_methods = (
            'announcements.add_announcement',
            'announcements.change_announcement',
            'announcements.delete_announcement',
            'announcements.view_announcement',
        )
        if not perm in allowed_methods:
            return False
        if not obj:
            # model permission
            if user_obj.is_authenticated():
                if user_obj.is_staff:
                    # If user is staff returns True permanently
                    return True
                elif perm == 'announcements.view_announcement':
                    return True
            return False
        # object permission
        if user_obj.is_staff:
            # all staffs can create / change / delete all announcements
            return True
        if perm == 'announcements.view_announcement' and obj:
            # check view perm by pub_state
            return self._has_view_perm(user_obj, perm, obj)
        return False