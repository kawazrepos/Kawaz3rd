from django.test import TestCase
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Star

class StarManagerTestCase(TestCase):

    def test_add_for_object(self):
        '''Tests add star to an object via add_for_object'''
        user = PersonaFactory()
        target = PersonaFactory()

        count = Star.objects.count()

        star = Star.objects.add_for_object(target, user)
        self.assertIsNotNone(star)
        self.assertTrue(Star.objects.count(), count + 1)


    def test_add_for_object_with_comment(self):
        '''Tests add star to an object with comment via add_for_object'''
        user = PersonaFactory()
        target = PersonaFactory()

        count = Star.objects.count()

        star = Star.objects.add_for_object(target, user, comment='イイネ!')
        self.assertIsNotNone(star)
        self.assertTrue(Star.objects.count(), count + 1)
        self.assertEqual(star.comment, 'イイネ!')

    def test_add_for_object_with_tag(self):
        '''Tests add star to an object with tag via add_for_object'''
        user = PersonaFactory()
        target = PersonaFactory()

        count = Star.objects.count()

        star = Star.objects.add_for_object(target, user, tag='red')
        self.assertIsNotNone(star)
        self.assertTrue(Star.objects.count(), count + 1)
        self.assertEqual(star.tag, 'red')

    def test_get_for_object(self):
        '''Tests get star for object via get_for_object'''
        user = PersonaFactory()
        user1 = PersonaFactory()
        user2 = PersonaFactory()

        for i in range(1): Star.objects.add_for_object(user, user)
        for i in range(2): Star.objects.add_for_object(user1, user)
        for i in range(3): Star.objects.add_for_object(user2, user)

        self.assertEqual(Star.objects.get_for_object(user).count(), 1)
        self.assertEqual(Star.objects.get_for_object(user1).count(), 2)
        self.assertEqual(Star.objects.get_for_object(user2).count(), 3)
        self.assertEqual(Star.objects.count(), 6)

    def test_cleanup_object(self):
        '''Tests clean up all stars via cleanup_object'''
        user = PersonaFactory()
        user1 = PersonaFactory()
        for i in range(1): Star.objects.add_for_object(user, user)
        for i in range(2): Star.objects.add_for_object(user1, user)
        self.assertEqual(Star.objects.count(), 3)

        Star.objects.cleanup_object(user)
        self.assertEqual(Star.objects.count(), 2)
