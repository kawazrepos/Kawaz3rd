from permission.logics import PermissionLogic


class ProjectPermissionLogic(PermissionLogic):
    def _has_join_perm(self, user_obj, perm, obj):
        if obj.pub_state == 'draft':
            # 下書きプロジェクトには誰も参加できない
            return False
        if not user_obj.is_authenticated():
            # 非認証ユーザーは参加不可
            return False
        if user_obj in obj.members.all():
            # 既に参加済みの場合は参加不可
            return False
        if user_obj.is_member:
            # メンバーであれば参加可能
            return True
        # それ以外（Wiile等）は参加不可
        return False

    def _has_quit_perm(self, user_obj, perm, obj):
        if user_obj == obj.administrator:
            # 管理者は退会不可
            return False
        if not user_obj.is_authenticated():
            # 非認証ユーザーは参加・不参加不可
            return False
        if user_obj not in obj.members.all():
            # 参加していないユーザは参加不可
            return False
        # それ以外の場合は参加可能（Willeチェックは不要）
        return True

    def has_perm(self, user_obj, perm, obj=None):
        """
        Check if user have a specified project permissions (of obj)
        """
        # 非承認ユーザーはあらゆる権限を持たない
        # Note: projects.view_project は別ロジックで定義
        if not user_obj.is_authenticated():
            return False
        # このロジックで処理するパーミッションを制限
        if perm not in ('projects.add_project',
                        'projects.change_project',
                        'projects.delete_project',
                        'projects.join_project',
                        'projects.quit_project'):
            return False
        if obj is None:
            # モデルパーミッション
            permissions = ('projects.add_project',
                           'projects.change_project',
                           'projects.delete_project',
                           'projects.join_project',
                           'projects.quit_project'
            )
            if perm in permissions and user_obj.is_member:
                # Seele, Nerv, Chidlren は下記パーミッションを持つ可能性がある
                return True
            return False
        # macros
        def author_required(user_obj, perm, obj):
            if not user_obj.is_member:
                return False
            return obj.administrator == user_obj
        # object permission
        permission_methods = {
            'projects.change_project': author_required,
            'projects.delete_project': author_required,
            'projects.join_project': self._has_join_perm,
            'projects.quit_project': self._has_quit_perm,
        }
        if perm in permission_methods:
            return permission_methods[perm](user_obj, perm, obj)
        return False
