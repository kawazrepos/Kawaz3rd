# coding=utf-8
"""
"""

from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ImproperlyConfigured
from kawaz.core.personas.tests.factories import PersonaFactory


class BasePermissionLogicTestCase(TestCase):
    app_label = None
    model_name = None
    # use_model_name指定が`True`のとき、自動的にperm名にmodel名を付けます
    # {app_label}.{perm}_{model_name}
    # `False`のとき、perm名をそのまま扱います
    # {app_label}.{perm}
    use_model_name = True

    def __init__(self, *args, **kwargs):
        # 指定が必要なアトリビュートのチェック
        exception_message = ("{} does not have a `{}` attribute. "
                             "The attribute is required to specify in class "
                             "level.")
        if not self.app_label:
            raise ImproperlyConfigured(exception_message.format(
                self.__class__.__name__, 'app_label'))
        if not self.model_name:
            raise ImproperlyConfigured(exception_message.format(
                self.__class__.__name__, 'model_name'))
        super().__init__(*args, **kwargs)

    def setUp(self):
        factory = lambda x: PersonaFactory(username=x, role=x)
        self.users = dict(
                adam=factory('adam'),
                seele=factory('seele'),
                nerv=factory('nerv'),
                children=factory('children'),
                wille=factory('wille'),
                anonymous=AnonymousUser(),
            )

    def _test(self, user, perm, obj=None, neg=False):
        """
        Test PermissionLogic

        Args:
            user (Persona instance or string): A persona instance of interest or string which indicates target role name
            perm (string): A permission string of interest
            obj (instance or None): An object of interest or None
            neg (bool): False for `assertTrue`, True for `assertFalse`
        """
        # if the specified user is string, find it from the dictionary
        if isinstance(user, str):
            user = self.users[user]
        username = 'anonymous'
        if user.is_authenticated():
            username = user.username
        # create full permission name
        if self.use_model_name:
            perm = "{}.{}_{}".format(self.app_label, perm, self.model_name)
        else:
            perm = "{}.{}".format(self.app_label, perm)
        # assert
        if not neg:
            self.assertTrue(user.has_perm(perm, obj=obj),
                            "{} should have '{}'".format(username, perm))
        else:
            self.assertFalse(user.has_perm(perm, obj=obj),
                             "{} should not have '{}'".format(username, perm))

