from permission.logics import PermissionLogic
from kawaz.core.utils.permission import check_object_permission


class CommentPermissionLogic(PermissionLogic):
    def _check_object_permissions(self, user_obj, codenames, obj):
        """
        指定されたユーザーが指定された省略形パーミッションのどれか一つでも
        対象オブジェクトに対して持つか調べる

        Args:
            user_obj (user instance): 対象ユーザー
            codenames (list or tuple): 省略形パーミッションリスト
            obj (model instance): 対象オブジェクト

        Returns:
            bool
        """
        def check(codename):
            r = check_object_permission(user_obj, codename, obj)
            if r is None:
                # パーミッションが存在しない場合はパーミッションを持つものと
                # して処理を行う
                return True
            return r
        if not isinstance(codenames, (list, tuple)):
            codenames = (codenames,)
        return any(check(codename) for codename in codenames)

    def has_perm(self, user_obj, perm, obj=None):
        """
        コメントのパーミッションを処理する

        Model permission:
            add: メンバーであれば True
            change: 誰も持たない
            delete: 誰も持たない
            can_moderate: メンバーであればTrue

        Object permission:
            change: 誰も持たない
            delete: 誰も持たない
            can_moderate: 以下のいずれかの条件を満たす
                - ネルフ権限以上がある
                - コメントの作者が自分である
                - 指定されたコメントがリンクしているオブジェクトの編集権限を持っている

        Notice:
            django_comments.can_moderateはdjango_comments.Commentが持つパーミッションであり
            commentのis_removedフラグを変更する権限である
        """

        # filter interest permissions
        if perm not in ('django_comments.add_comment',
                        'django_comments.change_comment',
                        'django_comments.delete_comment',
                        'django_comments.can_moderate'):
            return False
        if perm in ('django_comments.change_comment', 'django_comments.delete_comment'):
            # あらゆるユーザーがコメントの削除、変更不可能（神除く）
            return False
        if obj is None:
            permissions = ('django_comments.add_comment', 'django_comments.can_moderate',)
            if perm in permissions:
                if user_obj.is_authenticated() and user_obj.is_member:
                    # メンバーはコメントの付加、moderateが可能
                    return True
            return False
        # object permission
        if perm == 'django_comments.can_moderate':
            # コメントを非表示にする権限
            if user_obj.is_staff:
                # ネルフ権限以上であればmoderate可能
                return True
            elif obj.user == user_obj:
                # コメント作者はmoderate可能
                return True
            # それ以外の場合、対象オブジェクトの変更権限があればmoderate可能
            return self._check_object_permissions(user_obj, 'change',
                                                  obj.content_object)
        return False
