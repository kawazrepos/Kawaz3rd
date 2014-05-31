# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from permission.logics import PermissionLogic


class EventPermissionLogic(PermissionLogic):
    """
    Permission logic of Event model which for

    - `events.add_event`
    - `events.change_event`
    - `events.delete_event`
    - `events.attend_event`
    - `events.quit_event`

    """
    def _has_attend_perm(self, user_obj, perm, obj):
        # duplicated attendance is not permitted
        if obj.attendees.filter(pk=user_obj.pk):
            return False
        # 人数制限を超えていた場合は参加不可
        if obj.is_over_restriction():
            return False
        # 参加締め切りを過ぎていた場合は参加不可
        if obj.is_over_deadline():
            return False
        return True

    def _has_quit_perm(self, user_obj, perm, obj):
        # non attendee can quit the event
        if not obj.attendees.filter(pk=user_obj.pk):
            return False
        # the event organizer cannot quit the event
        if user_obj == obj.organizer:
            return False
        return True

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have a specified event permissions (of obj)
        """
        # anonymous use has no permissions
        if not user_obj.is_authenticated():
            return False
        # filter interest permissions
        if perm not in ('events.add_event',
                        'events.change_event',
                        'events.delete_event',
                        'events.attend_event',
                        'events.quit_event'):
            return False
        if obj is None:
            # generally, authenticated user have attend/quit permission
            if perm in ('events.attend_event', 'events.quit_event'):
                return True
            # seele, nerv, children have an add permission
            permissions = ('events.add_event',
                           'events.change_event',
                           'events.delete_event')
            roles = ('seele', 'nerv', 'children')
            if perm in permissions and user_obj.role in roles:
                # seele, nerv, children have permissions of add, change, event
                # generally
                return True
            return False

        # macros
        def author_required(user_obj, perm, obj):
            if user_obj.role not in ('seele', 'nerv', 'children'):
                return False
            return obj.organizer == user_obj
        # object permission
        permission_methods = {
            'events.change_event': author_required,
            'events.delete_event': author_required,
            'events.attend_event': self._has_attend_perm,
            'events.quit_event': self._has_quit_perm,
        }
        if perm in permission_methods:
            return permission_methods[perm](user_obj, perm, obj)
        return False


