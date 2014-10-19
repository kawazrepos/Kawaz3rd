from permission.logics import PermissionLogic
from kawaz.core.utils.permission import check_object_permission


class StarPermissionLogic(PermissionLogic):
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
        Starのパーミッションを処理する

        Model permission:
            add: メンバーであれば True
            change: 誰も持たない
            delete: メンバーであれば True
            view: 全員 True

        Object permission:
            add: メンバーかつ指定されたオブジェクトの閲覧権限があれば True
                詳細は後記
            change: 誰も持たない
            delete: メンバーかつ指定されたスターがリンクしている
                オブジェクトの閲覧権限があれば True
                もしくは指定されたスターがリンクしているオブジェクトの
                編集権限があれば True
            view: 指定されたスターがリンクしているオブジェクトの閲覧権限
                があれば True

        Notice:
            通常 add 権限は Model permission のみが存在するが、Star の場合は
            `has_perm`に付加対象オブジェクトを渡すことで付加対象オブジェクト
            に対する付加権限を調べることが可能
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
            return self._check_object_permissions(user_obj, 'view',
                                                  obj.content_object)
        elif perm == 'stars.add_star':
            # 渡されたオブジェクトにスターを付加する権限があるかを返す
            # 渡されたオブジェクトの閲覧権限を持っていればスターを付加する
            # 権限があるとする
            if user_obj.has_perm('stars.add_star'):
                return self._check_object_permissions(user_obj, 'view', obj)
            return False
        elif perm == 'stars.delete_star':
            # 循環参照を避けるためにここでStarモデルをロードしている
            from .models import Star
            if isinstance(obj, Star):
                if self._check_object_permissions(user_obj,
                                                  ('change', 'delete'),
                                                  obj.content_object):
                    # 付加先のコンテンツを編集可能な権限を持っている
                    # 場合は削除可能
                    return True
                if user_obj == obj.author:
                    # 自分が付加したスターは付加先のコンテンツの閲覧権限
                    # を持つ場合は削除可能
                    return self._check_object_permissions(user_obj,
                                                          'view',
                                                          obj.content_object)
            else:
                # 対象オブジェクトの編集権限を持つという事は
                # 対象オブジェクトに付加されたStarの削除権限を持つ
                return self._check_object_permissions(user_obj,
                                                      ('change', 'delete'),
                                                      obj)
        return False
