from django.core.exceptions import PermissionDenied
from django.test import TestCase
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.apps.blogs.tests.factories import EntryFactory
from ..models import Star
from .factories import StarFactory

class StarManagerTestCase(TestCase):
    def test_add_to_object(self):
        '''Tests add star to an object via add_to_object'''
        user = PersonaFactory()
        target = EntryFactory()

        count = Star.objects.count()

        star = Star.objects.add_to_object(target, user)
        self.assertIsNotNone(star)
        self.assertTrue(Star.objects.count(), count + 1)

    def test_add_to_object_with_comment(self):
        '''Tests add star to an object with comment via add_to_object'''
        user = PersonaFactory()
        target = EntryFactory()

        count = Star.objects.count()

        star = Star.objects.add_to_object(target, user, comment='イイネ!')
        self.assertIsNotNone(star)
        self.assertTrue(Star.objects.count(), count + 1)
        self.assertEqual(star.comment, 'イイネ!')

    def test_add_to_object_with_tag(self):
        '''Tests add star to an object with tag via add_to_object'''
        user = PersonaFactory()
        target = EntryFactory()

        count = Star.objects.count()

        star = Star.objects.add_to_object(target, user, tag='red')
        self.assertIsNotNone(star)
        self.assertTrue(Star.objects.count(), count + 1)
        self.assertEqual(star.tag, 'red')

    def test_remove_from_object(self):
        '''Tests remove_from_object works correctly'''
        object = EntryFactory()

        star = StarFactory(content_object=object)

        Star.objects.remove_from_object(object, star)
        self.assertEqual(Star.objects.get_for_object(object).count(), 0)

    def test_remove_from_object_with_wrong_object(self):
        '''Tests remove_from_object don't work correctly'''
        object = EntryFactory()
        star = StarFactory()

        self.assertRaises(AttributeError, Star.objects.remove_from_object, object, star)

    def test_get_for_object(self):
        '''Tests get star for object via get_for_object'''
        entry = EntryFactory()
        entry1 = EntryFactory()
        entry2 = EntryFactory()
        user = PersonaFactory()
        user1 = PersonaFactory()
        user2 = PersonaFactory()

        for i in range(1): StarFactory(content_object=entry, author=user)
        for i in range(2): StarFactory(content_object=entry1, author=user)
        for i in range(3): StarFactory(content_object=entry2, author=user)

        self.assertEqual(Star.objects.get_for_object(entry).count(), 1)
        self.assertEqual(Star.objects.get_for_object(entry1).count(), 2)
        self.assertEqual(Star.objects.get_for_object(entry2).count(), 3)
        self.assertEqual(Star.objects.count(), 6)

    def test_cleanup_object(self):
        '''Tests clean up all stars via cleanup_object'''
        entry = EntryFactory()
        entry1 = EntryFactory()
        user = PersonaFactory()

        for i in range(1): StarFactory(content_object=entry, author=user)
        for i in range(2): StarFactory(content_object=entry1, author=user)
        self.assertEqual(Star.objects.count(), 3)

        Star.objects.cleanup_object(entry)
        self.assertEqual(Star.objects.count(), 2)

class StarTestCase(TestCase):
    def test_author_can_not_change(self):
        '''Tests author can not change the star'''
        star = StarFactory()
        self.assertFalse(star.author.has_perm('stars.change_star', star))

    def test_others_can_not_change(self):
        '''Tests others can not change the star'''
        star = StarFactory()
        user = PersonaFactory()
        self.assertFalse(user.has_perm('stars.change_star', star))

    def test_author_can_delete(self):
        '''Tests author can delete the star'''
        star = StarFactory()
        self.assertTrue(star.author.has_perm('stars.delete_star', star))

    def test_others_can_not_delete(self):
        '''Tests others can not change the star'''
        star = StarFactory()
        user = PersonaFactory()
        self.assertFalse(user.has_perm('stars.change_star', star))

    def test_cant_add_star_to_unviewable_object(self):
        '''
        Tests users can't assign stars to unviewable object for them.
        e.g. if users attempt to add stars to other's draft blog entry, it will be raised PermissionDenied exception
        '''
        draftEntry = EntryFactory(pub_state='draft')
        user = PersonaFactory()
        self.assertRaises(PermissionDenied, StarFactory, content_object=draftEntry, author=user)
