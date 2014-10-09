# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/9
#
from kawaz.apps.blogs.forms import EntryForm
from kawaz.apps.blogs.tests.factories import CategoryFactory
from kawaz.core.personas.tests.factories import PersonaFactory

__author__ = 'giginet'
from django.test.testcases import TestCase

class EntryFormTestCase(TestCase):
    def test_category_queryset(self):
        """
        フォームのカテゴリ一覧にリクエストユーザーの物だけが含まれている
        """
        user = PersonaFactory()
        category = CategoryFactory(author=user)
        other_category = CategoryFactory()
        form = EntryForm(user=user)
        category_form = form.fields['category']
        # 未選択と自分の作った物の2つだけが含まれているはず
        self.assertEqual(len(category_form.choices), 2)
