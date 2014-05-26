from permission.logics import PermissionLogic

class RegistrationProfilePermissionLogic(PermissionLogic):
    def has_perm(self, user_obj, perm, obj=None):
        if not perm in (
            'registration.accept_registration',
            'registration.reject_registration',
            'registration.activate_user'
        ):
            return False
        if not user_obj.is_authenticated():
            # 非ログインユーザーは権限を持たない
            return False
        if user_obj.role in ['seele', 'nerv']:
            # Seele またはNervなら権限を持つ
            return True
        return False
