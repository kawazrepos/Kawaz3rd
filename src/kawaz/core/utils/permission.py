from django.core.exceptions import ObjectDoesNotExist
from permission.utils.permissions import perm_to_permission


def check_object_permission(user_obj, codename, obj):
    """
    指定ユーザが省略形パーミッションを指定オブジェクトに対して持つか調べる

    Args:
        user_obj (user instance): 対象ユーザインスタンス
        codename (str): 省略形パーミッション（例: `'add'`）
        obj (model instance): 対象モデルインスタンス

    Returns:
        bool or None: 指定されたパーミッションが存在する場合は`True`/`False`を
            返し、存在しない場合は`None`を返す
    """
    try:
        perm = get_full_permission_name(codename, obj)
        # 文字列 permission を実体に変換（してみる）
        perm_to_permission(perm)
        # 指定されたパーミッションが存在するためチェックを行う
        return user_obj.has_perm(perm, obj=obj)
    except ObjectDoesNotExist:
        # 指定されたパーミッションが存在しないため None を返す
        return None


def get_full_permission_name(codename, obj):
    """
    省略形パーミッションとオブジェクトからパーミッションの完全名を取得

    Args:
        codename (str): 省略形パーミッション（例: `'add'`）
        obj (model instance): 対象モデルインスタンス

    Returns:
        str: パーミッションの完全名（例: `'auth.add_user'`）
    """
    app_label = obj._meta.app_label
    model_name = obj._meta.object_name.lower()
    perm = '{}.{}_{}'.format(app_label, codename, model_name)
    return perm


def filter_with_perm(user_obj, qs, codename):
    """
    指定された省略形パーミッションを持つオブジェクトをフィルタリング

    Args:
        user_obj (user instance): 対象ユーザインスタンス
        qs (obj): QuerySetのインスタンスもしくはオブジェクトリスト
        codename (str): 省略形パーミッション（例: `'add'`）もしくは
            パーミッションの完全名

    Notice:
        `qs`にオブジェクトリストを渡す場合は`codename`はパーミッションの完全名
        である必要がある。
        また、この関数は全てのオブジェクトをいてレートするイテレータを返すため
        結果をリスト化する際に全てのオブジェクトを評価する。
        このためオブジェクト数が多い場合は計算時間がかかるので注意。

    Returns:
        iterator: フィルタしたオブジェクトイテレータ
    """
    if hasattr(qs, 'model'):
        perm = get_full_permission_name(codename, qs.model)
    else:
        perm = codename
    iterator = qs if isinstance(qs, (list, tuple)) else qs.iterator()
    iterator = filter(lambda x: user_obj.has_perm(perm, obj=x), iterator)
    return iterator
