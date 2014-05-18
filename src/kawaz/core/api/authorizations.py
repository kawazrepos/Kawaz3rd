from django.core.exceptions import ImproperlyConfigured
from tastypie.authorization import Authorization
from kawaz.core.permissions.utils import get_full_permission_name


def check_perm(bundle, perm, object_permission=False):
    """
    指定された権限をAPI使用ユーザが持っているか調べる

    Args:
        bundle (tastypie bundle instance): tastypieが使用するbundleインスタンス
        perm (string): パーミッションコード名（e.g. 'add'）
        object_permission (bool): オブジェクトパーミッションか否か

    Returns:
        bool: パーミッションを持っていればTrueを返す
    """
    perm = get_full_permission_name(perm, bundle.obj.__class__)
    user_obj = bundle.request.user
    obj = None if not object_permission else bundle.obj
    return user_obj.has_perm(perm, obj=obj)


def filter_with_perm(bundle, perm, object_list):
    """
    API使用ユーザーが指定されたパーミッションを所有するオブジェクトのみに
    フィルタリング

    Args:
        bundle (tastypie bundle instance): tastypieが使用するbundleインスタンス
        perm (string): パーミッションコード名（e.g. 'add'）
        object_list (list, tuple): フィルター元のオブジェクトリスト

    Returns:
        
    """
    perm = get_full_permission_name(perm, object_list.model)
    user_obj = bundle.request.user
    iterator = filter(lambda x: user_obj.has_perm(perm, obj=x), object_list)
    return list(iterator)


class PermissionBasedAuthorization(Authorization):
    """
    Create/Read/Update/Delete の権限を Permission から判別する
    Authorization クラス
    """
    def read_list(self, object_list, bundle):
        allowed = filter_with_perm(bundle, 'view', object_list)
        return allowed

    def read_detail(self, object_list, bundle):
        return check_perm(bundle, 'view', True)

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return check_perm(bundle, 'add', False)

    def update_list(self, object_list, bundle):
        allowed = filter_with_perm(bundle, 'change', object_list)
        return allowed

    def update_detail(self, object_list, bundle):
        return check_perm(bundle, 'change', True)

    def delete_list(self, object_list, bundle):
        allowed = filter_with_perm(bundle, 'delete', object_list)
        return allowed

    def delete_detail(self, object_list, bundle):
        return check_perm(bundle, 'delete', True)
