from django.db.models import Q


def published_lookup(user_obj, field_name='pub_state'):
    """
    指定されたユーザーが閲覧可能な公開オブジェクトをフィルタするための
    Qオブジェクトを返す

    ユーザーがメンバーであれば、publicおよびprotected指定のオブジェクトを返し
    それ以外であればpublic指定のオブジェクトを返す

    Args:
        user_obj (obj): Userモデルインスタンス（or AnonymousUser）
        field_name (str): 公開状態を指定しているフィールド名
            （デフォルト： ``'pub_state'``）

    Returns:
        Qオブジェクトインスタンス
    """
    q = Q(**{field_name: 'public'})
    if user_obj and user_obj.is_authenticated() and user_obj.is_member:
        q |= Q(**{field_name: 'protected'})
    return q


def draft_lookup(user_obj, author_field_name='author', field_name='pub_state'):
    """
    指定されたユーザーが編集可能な下書きオブジェクトをフィルタするための
    Qオブジェクトを返す

    ユーザーがメンバーであれば、自身が保有する下書き状態のオブジェクトを返し
    それ以外であれば何も返さない。なおユーザーがsuperuserの場合は存在する
    あらゆる下書き状態のオブジェクトを返す（superuserはあらゆる権限を持つため
    全ての下書き記事の編集権限を持つ）

    Args:
        user_obj (obj): Userモデルインスタンス（or AnonymousUser）
        author_field_name (str): 所有者を指定しているフィールド名
            （デフォルト: ``'author'``）
        field_name (str): 公開状態を指定しているフィールド名
            （デフォルト： ``'pub_state'``）
    Returns:
        Qオブジェクトインスタンス
    """
    # pk = -1 は db 的に存在しない値なので何も返さないフィルタになる
    q = Q(pk=-1)
    if user_obj and user_obj.is_authenticated():
        if user_obj.is_superuser:
            # superuser は全てのオブジェクトに対し編集権限を持つため所有者
            # チェックは行わない
            q = Q(**{field_name: 'draft'})
        elif user_obj.is_member:
            q = Q(**{author_field_name: user_obj, field_name: 'draft'})
    return q
