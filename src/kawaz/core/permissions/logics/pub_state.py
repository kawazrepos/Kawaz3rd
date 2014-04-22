from permission.logics import PermissionLogic
from django.utils.translation import ugettext as _

PUB_STATES = (
    ('public',      _("Public")),
    ('protected',   _("Internal")),
    ('draft',       _("Draft")),
)

class PubStatePermissionLogic(PermissionLogic):
    def __init__(self, author_field_name='author', pub_state_field_name='pub_state'):
        '''
        PermissionLogic to allow to see by its 'pub_state'.
        author_field_name : String
            the field name which indicates object's author. default value will be 'author'.
        pub_state_field_name : String
            the field name which indicates object's pub_state. default value will be 'pub_state'
        '''
        self.author_field_name = author_field_name
        self.pub_state_field_name = pub_state_field_name

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have permission (of object)

        Parameters
        ----------
        user_obj : django user model instance
            A django user model instance which be checked
        perm : string
            `app_label.codename` formatted permission string
        obj : None or django model instance
            None or django model instance for object permission

        Returns
        -------
        boolean
            Whether the specified user have specified permission (of specified
            object).

        .. note::
            Sub class must override this method.
        """
        if obj is None:
            # only treat object permission
            return False
        permission_name = self.get_full_permission_string('view')
        if perm == permission_name:
            author = getattr(obj, self.author_field_name, None)
            pub_state = getattr(obj, self.pub_state_field_name, '')
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
