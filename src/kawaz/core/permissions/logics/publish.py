from django.utils.translation import ugettext as _
from permission.logics import PermissionLogic

PUB_STATES = (
    ('public',      _("Public")),
    ('protected',   _("Internal")),
    ('draft',       _("Draft")),
)

class PubStatePermissionLogic(PermissionLogic):
    def __init__(self, author_field_name='author', publish_field_name='pub_state'):
        '''
        LogicPermission to allow to see by its 'pub_state'.
        '''
        self.field_name = author_field_name
        self.publish_field_name = publish_field_name

    def has_perm(self, user_obj, perm, obj=None):
        if obj is None:
            # only treat object permission
            return False
        permission_name = self.get_full_permission_string('view')
        if perm == permission_name:
            author = getattr(obj, self.field_name, None)
            pub_state = getattr(author, self.publish_field_name, '')
            if pub_state == 'public':
                # if pub_state is public, everyone see this object
                return True
            elif pub_state == 'protected':
                # if pub_state is protected, users who logged in and role isn't wille see this object
                return user_obj and user_obj.is_authenticated() and user_obj.role != 'wille'
            elif pub_state == 'draft':
                # if pub_state is draft, Only author can see this object.
                return author == user_obj
        return False