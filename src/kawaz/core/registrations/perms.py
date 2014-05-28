from permission.logics import PermissionLogic


class RegistrationProfilePermissionLogic(PermissionLogic):
    def has_perm(self, user_obj, perm, obj=None):
        if perm not in (
            'registration.add_registrationprofile',
            'registration.change_registrationprofile',
            'registration.delete_registrationprofile',
            'registration.accept_registration',
            'registration.reject_registration',
            'registration.activate_user'
        ):
            return False
        if perm == 'registration.add_registrationprofile':
            # registrationの作成は全てのユーザーが可能である
            return True
        if not user_obj.is_authenticated():
            # 非ログインユーザーは権限を持たない
            return False
        if user_obj.role in ['seele', 'nerv']:
            # Seele またはNervなら権限を持つ
            return True
        return False
