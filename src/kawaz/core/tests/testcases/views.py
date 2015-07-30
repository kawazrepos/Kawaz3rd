# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/8/19
#
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from django.test import TestCase



class BaseViewPermissionTestCase(TestCase):

    def setUp(self):
        self.members = (
                PersonaFactory(role='adam'),
                PersonaFactory(role='seele'),
                PersonaFactory(role='nerv'),
                PersonaFactory(role='children'),
            )
        self.non_members = (
                PersonaFactory(role='wille'),
                AnonymousUser(),
            )

    def prefer_login(self, user):
        if user.is_authenticated():
            self.assertTrue(self.client.login(username=user.username,
                                              password='password'))
