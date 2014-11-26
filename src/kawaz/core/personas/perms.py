from permission.logics import PermissionLogic
from permission.logics import AuthorPermissionLogic


class PersonaPermissionLogic(PermissionLogic):
    """
    Persona操作に関係するパーミッションロジック

    add_persona:
        ゼーレ権限以上のみ権限を持つ
    change_persona:
        自分自身以外には権限を持たない
    delete_persona:
        スーパーユーザー以外は権限を持たない
    activate_persona:
        ネルフ権限以上のみ持つ
    assign_role_persona:
        ゼーレ権限以上のみ権限を持つ
    """
    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active or not user_obj.is_authenticated():
            return False
        if perm == 'personas.add_persona':
            # ゼーレ以上の場合は追加権限を持つ
            return user_obj.role in ('adam', 'seele')
        elif perm == 'personas.change_persona':
            # 自分自身の場合は編集権限を持つ
            return obj is None or (obj == user_obj and user_obj.is_member)
        elif perm == 'personas.activate_persona':
            # スタッフ以上の場合はアクティベート権限を持つ
            return user_obj.is_staff
        elif perm == 'personas.assign_role_persona':
            # ゼーレ以上の場合は役職変更権限を持つ
            return user_obj.role in ('adam', 'seele')
        return False


class RoleBasedAuthorPermissionLogic(AuthorPermissionLogic):
    """
    特定の役職に含まれていた場合のみ機能する AuthorPermissionLogic
    """
    accepted_roles = ('adam', 'seele', 'nerv', 'children')

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active or not user_obj.is_authenticated():
            return False
        if user_obj.role not in self.accepted_roles:
            return False
        return super().has_perm(user_obj, perm, obj)


class RoleBasedPermissionLogic(PermissionLogic):
    """
    特定の役職に含まれているかどうかで判断を行うパーミッションロジック
    """
    accepted_roles = ()

    def __init__(self,
                 any_permission=False,
                 add_permission=False,
                 change_permission=False,
                 delete_permission=False):
        """
        コンストラクタ

        Parameters
        ----------
        any_permission : boolean
            これがTrueの場合はあらゆる権限を持つとして扱われる
        add_permission : boolean
            追加権限を持つか否か
        change_permission : boolean
            更新権限を持つか否か
        delete_permission : boolean
            削除権限を持つか否か
        """
        self.any_permission = any_permission
        self.add_permission = add_permission
        self.change_permission = change_permission
        self.delete_permission = delete_permission

    def has_perm(self, user_obj, perm, obj=None):
        """
        user_obj.role を基準に与えられた権限を持つか調べる

        モデル権限（オブジェクト指定なし）の場合は指定された権限を持つ可能性
        がある場合はTrueを返す（従って any_permission が指定されている場合は
        あらゆる権限に対し True を返す）

        Parameters
        ----------
        user_obj : django user model instance
            Djangoのユーザーモデルインスタンス
        perm : string
            'app_label.codename'というフォーマットの権限文字列
        obj : None or django model instance
            オブジェクトパーミッションの対象となるオブジェクト

        Returns
        -------
        boolean
            指定された権限をユーザーが持つか否か
        """
        if not user_obj.is_active or not user_obj.is_authenticated():
            return False
        add_name = self.get_full_permission_string('add')
        change_name = self.get_full_permission_string('change')
        delete_name = self.get_full_permission_string('delete')
        if obj is None:
            if self.any_permission and user_obj.role in self.accepted_roles:
                return True
            if ((self.add_permission and perm == add_name) or
                    (self.change_permission and perm == change_name) or
                    (self.delete_permission and perm == delete_name)):
                return user_obj.role in self.accepted_roles
            return False
        else:
            if user_obj.role in self.accepted_roles:
                if self.any_permission:
                    return True
                if self.change_permission and perm == change_name:
                    return True
                if self.delete_permission and perm == delete_name:
                    return True
        return False


class ChildrenPermissionLogic(RoleBasedPermissionLogic):
    """
    Children以上のユーザーに対して権限を与えるパーミッションロジック
    """
    accepted_roles = ('adam', 'seele', 'nerv', 'children')


class NervPermissionLogic(RoleBasedPermissionLogic):
    """
    Nerv以上のユーザーに対して権限を与えるパーミッションロジック
    """
    accepted_roles = ('adam', 'seele', 'nerv')


class SeelePermissionLogic(RoleBasedPermissionLogic):
    """
    Seele以上のユーザーに対して権限を与えるパーミッションロジック
    """
    accepted_roles = ('adam', 'seele')
