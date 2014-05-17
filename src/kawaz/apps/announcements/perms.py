from permission.logics import PermissionLogic


class AnnouncementPermissionLogic(PermissionLogic):
    """
    Announcementの権限クラス

    スタッフユーザーはあらゆる権限を持ち、それ以外は記事の状態とメンバーか否か
    により閲覧権限が変わる
    """
    def has_perm(self, user_obj, perm, obj=None):
        allowed_methods = (
            'announcements.add_announcement',
            'announcements.change_announcement',
            'announcements.delete_announcement',
            'announcements.view_announcement',
        )
        if not perm in allowed_methods:
            return False
        if obj:
            # object permission
            if user_obj.is_staff:
                # スタッフはAnnouncementに対してあらゆる権限を持つ
                return True
            elif perm == 'announcements.view_announcement':
                # 閲覧権限はある可能性がある
                return self._has_view_perm(user_obj, perm, obj)
            # スタッフ以外は閲覧権限以外は持たない
            return False
        else:
            # model permission
            if user_obj.is_staff:
                # スタッフはAnnouncementに対してあらゆる権限を持つ
                return True
            elif perm == 'announcements.view_announcement':
                # 閲覧権限は持つ可能性があるのでモデルレベルでは恒常的にTrue
                return True
            return False

    def _has_view_perm(self, user_obj, perm, obj):
        if obj.pub_state == 'protected':
            # メンバーだけが内部公開記事を閲覧可能
            return user_obj.is_authenticated() and user_obj.is_member
        if obj.pub_state == 'draft':
            # 下書きを閲覧できるのはスタッフユーザのみ
            return user_obj.is_staff
        return True

