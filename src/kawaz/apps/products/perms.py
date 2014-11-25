from permission.logics import PermissionLogic


class ProductPermissionLogic(PermissionLogic):

    def _has_join_perm(self, user_obj, perm, obj=None):
        if not user_obj.is_authenticated:
            # 非ログインユーザーは参加できない
            return False
        elif not user_obj.is_member:
            # メンバー以外は参加できない
            return False
        elif obj and user_obj in obj.administrators.all():
            # 既に参加済みのユーザーは参加できない
            return False
        return True

    def _has_quit_perm(self, user_obj, perm, obj=None):
        if not user_obj in obj.administrators.all():
            # 参加してないユーザーは脱退できない
            return False
        elif obj.administrators.count() == 1:
            # 最後の一人は脱退できない
            return False
        return True

    def has_perm(self, user_obj, perm, obj=None):
        if not perm in (
            'products.add_product',
            'products.change_product',
            'products.delete_product',
            'products.join_product',
            'products.quit_product'
        ):
            return False
        if not user_obj.is_authenticated():
            # Anonymous Userはパーミッションを持たない
            return False
        if not user_obj.is_member:
            # メンバー以外はパーミッションを持たない
            return False
        if obj:
            # オブジェクトパーミッション
            if perm == 'products.change_product':
                if user_obj in obj.administrators.all():
                    # 管理者ならTrue
                    return True
                elif user_obj.is_staff:
                    # ネルフ以上ならTrue
                    return True
                elif obj.project and user_obj in obj.project.members.all():
                    # プロジェクトメンバーならTrue
                    return True
            elif perm == 'products.delete_product':
                return user_obj in obj.administrators.all()
            elif perm == 'products.join_product':
                return self._has_join_perm(user_obj, perm, obj)
            elif perm == 'products.quit_product':
                return self._has_quit_perm(user_obj, perm, obj)
        else:
            return True
        return False
