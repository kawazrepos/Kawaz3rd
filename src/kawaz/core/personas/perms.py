# coding=utf-8
"""
"""

from permission.logics import PermissionLogic
from permission.logics import AuthorPermissionLogic


class PersonaPermissionLogic(PermissionLogic):
    """
    Permission logics which check the user's role and return corresponding
    permission
    """
    def _has_add_perm(self, user_obj, perm, obj):
        # ゼーレ権限以上のスタッフのみ手作業でユーザーを追加可能
        # （ユーザーの手動追加はAdminページのみで可能）
        return user_obj.role in ('adam', 'seele',)

    def _has_change_perm(self, user_obj, perm, obj):
        # 自分自身のPersonaのみ編集権限を持つ
        if obj is None:
            # Non object permission
            return user_obj.is_member
        else:
            return (obj == user_obj and user_obj.is_member)

    def _has_delete_perm(self, user_obj, perm, obj):
        # スーパーユーザー以外は削除権限を持たない
        return False

    def _has_activate_perm(self, user_obj, perm, obj):
        # ネルフ権限以上のスタッフのみ手作業でユーザーのアクティベイト
        # が可能（Adminページ限定）
        return user_obj.role in ('seele', 'nerv',)

    def _has_view_grave_perm(self, user_obj, perm, obj):
        return user_obj.role in ('children', 'seele', 'nerv')

    def _has_assign_role_perm(self, user_obj, perm, obj):
        # ゼーレ権限以上の場合のみ役職を変更することができる
        return user_obj.role in ('seele',)

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_authenticated():
            return False
        permission_methods = {
            'personas.add_persona': self._has_add_perm,
            'personas.change_persona': self._has_change_perm,
            'personas.delete_persona': self._has_delete_perm,
            'personas.activate_persona': self._has_activate_perm,
            'personas.assign_role_persona': self._has_assign_role_perm,
            'personas.view_grave': self._has_view_grave_perm,
        }
        if perm in permission_methods:
            return permission_methods[perm](user_obj, perm, obj)
        return False


class BaseRolePermissionLogic(PermissionLogic):
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
            True for give any permission of the specified object or model to
            the role. Default value will be `False`
        add_permission : boolean
            True for give add permission of the specified model to the role.
            Default value will be 'False'
        change_permission : boolean
            True for give change permission of the specified object to the
            role.  Default value will be 'False'
        delete_permission : boolean
            True for give delete permission of the specified object to the
            role. Default value will be 'False'
        """
        self.any_permission = any_permission
        self.add_permission = add_permission
        self.change_permission = change_permission
        self.delete_permission = delete_permission

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have permission (of object)
        It is determined from the `user_obj.role`.

        If no object is specified, if any_permission is True it returns
        ``True``.  if else returns ``False``.

        If an object is specified, it will return ``True`` if the user's role
        is contained in ``role_names``.

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
        add_name = self.get_full_permission_string('add')
        change_name = self.get_full_permission_string('change')
        delete_name = self.get_full_permission_string('delete')
        if not user_obj.is_active:
            return False
        role = getattr(user_obj, 'role', None)
        if obj is None:
            if self.any_permission and role in self.role_names:
                return True
            if self.add_permission and perm == add_name:
                if role and role in self.role_names:
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


class ChildrenPermissionLogic(BaseRolePermissionLogic):
    """
    Permission logic class to allow permissions to over `Children` role user.
    """
    role_names = ['adam', 'seele', 'nerv', 'children']


class NervPermissionLogic(BaseRolePermissionLogic):
    """
    Permission logic class to allow permissions to over `Nerv`(staff) role user
    """
    role_names = ['adam', 'seele', 'nerv']


class SeelePermissionLogic(BaseRolePermissionLogic):
    """
    Permission logic class to allow permissions to over `Seele` role user.
    """
    role_names = ['adam', 'seele']


class AdamPermissionLogic(BaseRolePermissionLogic):
    """
    Permission logic class to allow permissions to over `Adam`(superuser) role
    user
    """
    role_names = ['adam']


class KawazAuthorPermissionLogic(AuthorPermissionLogic):
    """
    Kawaz用AuthorPermissionLogic

    Kawazの仕様では、willeがauthorになることは現段階ではない。
    通常のAuthorPermissionLogicを利用すると、willeであっても
    ログインユーザーであればモデルパーミッションがTrueになり
    使い勝手が悪い
    そのため、wille以下の場合はFalseが返るようにした
    """
    role_names = ['adam', 'seele', 'nerv', 'children']

    def has_perm(self, user_obj, perm, obj=None):
        if (user_obj.is_authenticated() and
            user_obj.role not in self.role_names):
            return False
        return super().has_perm(user_obj, perm, obj)
