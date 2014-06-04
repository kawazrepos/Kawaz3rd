from django.contrib.auth.models import AnonymousUser
from .factories import PersonaFactory


def create_role_users(extras=None):
    """
    権限テストの際などに便利な各roleを持つユーザーを格納した辞書を作成

    各ユーザーはrole名をusernameに持ち、role名をキーとした辞書に格納された
    状態で返される。既存の辞書を拡張するには`extras`を指定する。

    Args:
        extras (None or dict): 追加するユーザーが格納された辞書

    Returns:
        dict

    Examples:
        >>> users = create_role_users()
        >>> assert set(users.keys()) == set((
        ...     'adam', 'seele', 'nerv', 'children',
        ...     'wille', 'anonymous',
        ... ))
        >>> for role, user in users.items():
        ...     assert role == user.username
    """
    factory = lambda x: PersonaFactory(username=x, role=x)
    users = dict(
        adam=factory('adam'),
        seele=factory('seele'),
        nerv=factory('nerv'),
        children=factory('children'),
        wille=factory('wille'),
        anonymous=AnonymousUser(),
    )
    if extras is not None:
        users.update(extras)
    return users
