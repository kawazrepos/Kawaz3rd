from permission.logics import PermissionLogic
from permission.utils.field_lookup import field_lookup


class PublishmentPermissionLogic(PermissionLogic):
    """
    Permission logic of AbstractPublishmentModel subclass.
    This permission logic handle the 'view' permission based on the publishment
    status
    """
    def __init__(self, author_field_name='author',
                 pub_state_field_name='pub_state'):
        """
        PermissionLogic to allow to see by its 'pub_state'.

        Parameters
        ----------
        author_field_name : str
            The field name of author in the model.
            The default value is 'author'.
        pub_state_field_name : str
            The field name of publishment status in the model.
            The default value is 'pub_state'
        """
        self.author_field_name = author_field_name
        self.pub_state_field_name = pub_state_field_name

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have `view` permission (of object) based on the
        ``pub_state`` and ``author`` of the instance.

        If no object is specified, it always return ``True``.

        If an object is specified, it will return ``True`` when the
        ``pub_state`` of the instance is:

        - 'public'    | Anyone can see this obj
        - 'protected' | Seele, Nerv, Children can see this obj
        - 'draft'     | Nobody but the obj author can see this obj

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
            Wheter the specified user have specified permission (of specified
            object).
        """
        # construct the permission name
        permission_name = self.get_full_permission_string('view')
        # everybody have a potential to see the model
        if obj is None:
            return perm == permission_name
        if perm == permission_name:
            author = field_lookup(obj, self.author_field_name)
            pub_state = field_lookup(obj, self.pub_state_field_name)
            if pub_state == 'public':
                # if pub_state is public, everyone see this object
                return True
            elif pub_state == 'protected':
                # if pub_state is protected, users who logged in and role isn't
                # wille see this object
                return user_obj.is_authenticated() and user_obj.is_member
            elif pub_state == 'draft':
                # if pub_state is draft, Only author can see this object.
                return author == user_obj
        return False
