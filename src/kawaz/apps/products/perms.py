from permission.logics import PermissionLogic


class ProductPermissionLogic(PermissionLogic):
    allowed_permissions = (
        'products.add_product',
        'products.change_product',
        'products.delete_product',
        'products.join_product',
        'products.quit_product',
    )

    def has_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_active or not user_obj.is_authenticated():
            return False
        if not user_obj.is_member:
            return False
        if perm not in self.allowed_permissions:
            return False
        if obj:
            if perm == 'products.change_product':
                if user_obj.is_staff or user_obj in obj.administrators.all():
                    # スタッフもしくは対象プロダクトの管理メンバーならば
                    # 編集権限を所有
                    return True
                elif obj.project and user_obj in obj.project.members.all():
                    # プロジェクトメンバーならTrue
                    return True
            elif perm == 'products.delete_product':
                # 対象プロダクトの管理メンバーならば削除権限を所有
                return user_obj in obj.administrators.all()
            elif perm == 'products.join_product':
                # 既に管理者として参加済みのユーザーは参加不可
                return user_obj not in obj.administrators.all()
            elif perm == 'products.quit_product':
                if obj.administrators.count() == 1:
                    # 管理者不在を防ぐため最後の管理者は辞退不可
                    return False
                return user_obj in obj.administrators.all()
            return False
        else:
            # すべてのメンバーは allowed_permissions で指定されたモデル権限
            # を所有している
            return True
