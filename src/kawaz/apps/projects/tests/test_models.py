from django.test import TestCase
from django.contrib.auth.models import Group

from .factories import ProjectFactory, CategoryFactory
from kawaz.core.auth.tests.factories import UserFactory


class CategoryTestCase(TestCase):
    def test_str(self):
        '''Tests __str__ returns correct value'''
        category = CategoryFactory()
        self.assertEqual(category.__str__(), category.label)

class ProjectTestCase(TestCase):
    def test_create_group(self):
        '''Tests to create a group when project was created'''
        project = ProjectFactory()
        group_name = 'project_%s' % project.slug
        group = Group.objects.get(name=group_name)
        self.assertIsNotNone(group)

    def test_str(self):
        '''Tests __str__ returns correct value'''
        project = ProjectFactory()
        self.assertEqual(project.__str__(), project.title)

    def test_join_user(self):
        '''Tests can join user correctly'''
        user2 = UserFactory()
        project = ProjectFactory()
        self.assertEqual(project.members.count(), 1)
        self.assertEqual(user2.groups.count(), 0)

        project.join_member(user2)

        self.assertEqual(project.members.count(), 2)
        self.assertEqual(user2.groups.count(), 1)

    def test_is_member(self):
        '''Tests is_member returns correct value'''
        user = UserFactory()
        user2 = UserFactory()
        project = ProjectFactory(administrator=user)
        self.assertEqual(project.members.count(), 1)
        self.assertEqual(project.members.all()[0], user)
        self.assertTrue(project.is_member(user))
        self.assertFalse(project.is_member(user2))

    def test_administrator_is_member(self):
        '''Tests administrator will be added into member automatically'''
        user = UserFactory()
        project = ProjectFactory(administrator=user)
        self.assertTrue(project.is_member(user))

    def test_quit_member(self):
        '''Tests can remove member correctly'''
        project = ProjectFactory()
        user = UserFactory()

        project.join_member(user)
        self.assertEqual(project.members.count(), 2)

        project.quit_member(user)
        self.assertEqual(project.members.count(), 1)
        self.assertFalse(user in user.groups.all())

    def test_administrator_cant_quit(self):
        '''Tests administrator can't quit from projects'''
        project = ProjectFactory()

        def quit():
            project.quit_member(project.administrator)
        self.assertRaises(AttributeError, quit)

    def test_not_member_cant_quit(self):
        '''Tests non member can't quit from projects'''
        project = ProjectFactory()
        user = UserFactory()

        def quit():
            project.quit_member(user)
        self.assertRaises(AttributeError, quit)
