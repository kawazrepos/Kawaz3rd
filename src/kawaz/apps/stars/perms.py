from django.core.exceptions import ObjectDoesNotExist
from permission.logics import PermissionLogic
from permission.utils.permissions import perm_to_permission
from kawaz.core.utils.permission import get_full_permission_name


class StarPermissionLogic(PermissionLogic):
    def _has_perm_of_content_object(self, user_obj, perm, obj,
                                    content_object=True):
        """
        スター付加先のオブジェクトの公開状態をチェックし、内部公開であれば
        ユーザーにその記事の閲覧権限があるかどうかによりスターの閲覧権限を
        規定する
        """
        try:
            if content_object:
                obj = obj.content_object
            # 対象オブジェクトのパーミッションを取得
            perm = get_full_permission_name(perm, obj)
            # 文字列 permission を実体に変換
            perm_to_permission(perm)
            # 指定されたパーミッションが存在するためチェックを行う
            return user_obj.has_perm(perm, obj=obj)
        except ObjectDoesNotExist:
            # 指定されたパーミッションが存在しない。
            # Star自体に閲覧権限があるわけではないので、今場合は常にTrue
            return True

    def has_perm(self, user_obj, perm, obj=None):
        """
        Starのパーミッションを処理する

        add - 全てのメンバーが持つ
        change - 誰も持たない
        delete - 所有者のみ持つ
        view - 付加対象の公開状態依存
        """

        # filter interest permissions
        if perm not in ('stars.add_star',
                        'stars.change_star',
                        'stars.delete_star',
                        'stars.view_star'):
            return False
        if perm == 'stars.change_star':
            # nobody can change stars
            return False
        if obj is None:
            permissions = ('stars.add_star', 'stars.delete_star',)
            if perm in permissions:
                if user_obj.is_authenticated() and user_obj.is_member:
                    # メンバーはスターの付加・削除が可能
                    return True
            if perm == 'stars.view_star':
                # あらゆるユーザがスターを見る権利を持つ可能性がある
                return True
            return False
        # object permission
        if perm == 'stars.view_star':
            # 基本的に全てのスターは誰でも見ることができ、Starそのものには
            # 公開状態がないが、このチェックをしないと非公開オブジェクトの
            # StarがpublicなAPIで取れてしまって引用などが見られてしまう
            # 可能性があるので、content_objectが見れる場合のみ閲覧権限がある
            return self._has_perm_of_content_object(user_obj, 'view', obj)
        elif perm == 'stars.add_star':
            # 渡されたオブジェクトにスターを付加する権限があるかを返す
            # 渡されたオブジェクトの閲覧権限を持っていればスターを付加する
            # 権限があるとする
            if user_obj.has_perm('stars.add_star'):
                return self._has_perm_of_content_object(user_obj, 'view', obj,
                                                        content_object=False)
            return False
        elif perm == 'stars.delete_star':
            if self._has_perm_of_content_object(user_obj, 'change', obj):
                # 付加先のコンテンツを編集可能な権限を持っている場合も削除可能
                return True
            elif self._has_perm_of_content_object(user_obj, 'delete', obj):
                # 付加先のコンテンツを削除可能な権限を持っている場合も削除可能
                return True
            if user_obj == obj.author:
                # 自分が付加したスターは付加先のコンテンツの閲覧権限を持つ場合
                # は可能
                return self._has_perm_of_content_object(user_obj, 'view', obj)
        return False
