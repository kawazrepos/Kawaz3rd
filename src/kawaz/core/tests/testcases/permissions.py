# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory


class BasePermissionLogicTestCase(TestCase):
    app_label = None
    model_name = None

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
            user (Persona instance): A persona instance of interest
            perm (string): A permission string of interest
            obj (instance or None): An object of interest or None
            neg (bool): False for `assertTrue`, True for `assertFalse`
        """
        # if the specified user is string, find it from the dictionary
        if isinstance(user, str):
            user = self.users[user]
        # create full permission name
        perm = "{}.{}_{}".format(self.app_label, perm, self.model_name)
        # assert
        if not neg:
            self.assertTrue(user.has_perm(perm, obj=obj),
                            "{} should have '{}'".format(user.username, perm))
        else:
            self.assertFalse(user.has_perm(perm, obj=obj),
                             "{} should not have '{}'".format(user.username, perm))

