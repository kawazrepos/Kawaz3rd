from django.test import TestCase
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.apps.blogs.tests.factories import EntryFactory
from ..models import Star
from .factories import StarFactory


class StarManagerTestCase(TestCase):
    def test_add_to_object(self):
        """スターの追加テスト"""
        user = PersonaFactory()
        target = EntryFactory()

        count = Star.objects.count()

        star = Star.objects.add_to_object(target, user)
        self.assertIsNotNone(star)
        self.assertTrue(Star.objects.count(), count + 1)

    def test_add_to_object_with_quote(self):
        """スターの追加テスト（引用付き）"""
        user = PersonaFactory()
        target = EntryFactory()

        count = Star.objects.count()
        quote = "テスト"

        star = Star.objects.add_to_object(target, user, quote=quote)
        self.assertIsNotNone(star)
        self.assertTrue(Star.objects.count(), count + 1)
        self.assertEqual(star.quote, quote)

    def test_remove_from_object(self):
        """スターの削除テスト"""
        obj = EntryFactory()

        star = StarFactory(content_object=obj)

        Star.objects.remove_from_object(obj, star)
        self.assertEqual(Star.objects.get_for_object(obj).count(), 0)

    def test_remove_from_object_with_wrong_object(self):
        """
        指定したスターが指定したオブジェクトに存在しない場合は
        ObjectDoesNotExist が発生する
        """
        obj = EntryFactory()
        star = StarFactory()
        self.assertRaises(ObjectDoesNotExist,
                          Star.objects.remove_from_object, obj, star)

    def test_get_for_object(self):
        """指定されたオブジェクトに関連付けられたスターを取得するテスト"""
        entry1 = EntryFactory()
        entry2 = EntryFactory()
        entry3 = EntryFactory()
        user1 = PersonaFactory()
        user2 = PersonaFactory()
        user3 = PersonaFactory()

        for i in range(1):
            StarFactory(content_object=entry1, author=user1)
        for i in range(2):
            StarFactory(content_object=entry2, author=user2)
        for i in range(3):
            StarFactory(content_object=entry3, author=user3)

        self.assertEqual(Star.objects.get_for_object(entry1).count(), 1)
        self.assertEqual(Star.objects.get_for_object(entry2).count(), 2)
        self.assertEqual(Star.objects.get_for_object(entry3).count(), 3)
        self.assertEqual(Star.objects.count(), 6)

    def test_cleanup_object(self):
        """指定されたオブジェクトからスターを全て取り除くテスト"""
        entry1 = EntryFactory()
        entry2 = EntryFactory()
        user = PersonaFactory()

        for i in range(1):
            StarFactory(content_object=entry1, author=user)
        for i in range(2):
            StarFactory(content_object=entry2, author=user)

        self.assertEqual(Star.objects.count(), 3)
        Star.objects.cleanup_object(entry2)
        self.assertEqual(Star.objects.count(), 1)

