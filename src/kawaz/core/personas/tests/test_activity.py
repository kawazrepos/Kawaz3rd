# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/18
#
from django.template import Context
from activities.models import Activity
from activities.registry import registry
from .factories import PersonaFactory
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase

__author__ = 'giginet'


class PersonaActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = PersonaFactory

    def test_update(self):
        self._test_partial_update(('nickname_updated', 'gender_updated', 'avatar_created', 'is_active_deleted'),
                                  nickname='ニックネーム変えました',
                                  gender='man',
                                  avatar='icon.png',
                                  is_active=False)

    def test_add_comment(self):
        self._test_add_comment()
