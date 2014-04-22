from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from .factories import ProfileFactory, AccountFactory, ServiceFactory, SkillFactory

class ProfileViewPermissionTestCase(TestCase):
    def test_owner_can_view_protected(self):
        '''Tests owner can view protected'''
        profile = ProfileFactory(pub_state='protected')
        self.assertTrue(profile.user.has_perm('profiles.view_profile', profile))

    def test_others_can_view_protected(self):
        '''Tests others can view protected'''
        user = PersonaFactory()
        profile = ProfileFactory(pub_state='protected')
        self.assertTrue(user.has_perm('profiles.view_profile', profile))

    def test_anonymous_can_not_view_protected(self):
        '''Tests anonymous can not view protected'''
        user = AnonymousUser()
        profile = ProfileFactory(pub_state='protected')
        self.assertFalse(user.has_perm('profiles.view_profile', profile))

    def test_owner_can_view_public(self):
        '''Tests owner can view public'''
        profile = ProfileFactory(pub_state='public')
        self.assertTrue(profile.user.has_perm('profiles.view_profile', profile))

    def test_others_can_view_public(self):
        '''Tests others can view public'''
        user = PersonaFactory()
        profile = ProfileFactory(pub_state='public')
        self.assertTrue(user.has_perm('profiles.view_profile', profile))

    def test_anonymous_can_not_view_public(self):
        '''Tests anonymous can view public'''
        user = AnonymousUser()
        profile = ProfileFactory(pub_state='public')
        self.assertTrue(user.has_perm('profiles.view_profile', profile))


class SkillPermissionTestCase(TestCase):
    def setUp(self):
        self.users = dict(
                adam=PersonaFactory(role='adam'),
                seele=PersonaFactory(role='seele'),
                nerv=PersonaFactory(role='nerv'),
                children=PersonaFactory(role='children'),
                wille=PersonaFactory(role='wille'),
            )
        self.skill = SkillFactory()
        self.user = PersonaFactory()

    def _test_permission(self, role, perm, obj=None, negative=False):
        user = self.users.get(role)
        perm = "profiles.{}_skill".format(perm)
        if negative:
            self.assertFalse(user.has_perm(perm, obj=obj),
                "{} should not have '{}'".format(role.capitalize(), perm))
        else:
            self.assertTrue(user.has_perm(perm, obj=obj),
                "{} should have '{}'".format(role.capitalize(), perm))

    def test_seele_can_add_skill(self):
        '''Tests seele users can add new skills'''
        self._test_permission('seele', 'add')

    def test_nerv_can_add_skill(self):
        '''Tests seele users can add new skills'''
        self._test_permission('nerv', 'add')

    def test_children_cannot_add_skill(self):
        '''Tests seele users can add new skills'''
        self._test_permission('children', 'add', negative=True)

    def test_wille_cannnot_add_skill(self):
        '''Tests seele users can add new skills'''
        self._test_permission('wille', 'add', negative=True)

    def test_seele_can_change_skill(self):
        '''Tests seele users can change exist skills'''
        self._test_permission('seele', 'change', obj=self.skill)

    def test_nerv_can_change_skill(self):
        '''Tests seele users can change exist skills'''
        self._test_permission('nerv', 'change', obj=self.skill)

    def test_children_cannot_change_skill(self):
        '''Tests seele users can change exist skills'''
        self._test_permission('children', 'change', obj=self.skill, negative=True)

    def test_wille_cannnot_change_skill(self):
        '''Tests seele users can change exist skills'''
        self._test_permission('wille', 'change', obj=self.skill, negative=True)

    def test_seele_can_delete_skill(self):
        '''Tests seele users can delete exist skills'''
        self._test_permission('seele', 'delete', obj=self.skill)

    def test_nerv_can_delete_skill(self):
        '''Tests seele users can delete exist skills'''
        self._test_permission('nerv', 'delete', obj=self.skill)

    def test_children_cannot_delete_skill(self):
        '''Tests seele users can delete exist skills'''
        self._test_permission('children', 'delete', obj=self.skill, negative=True)

    def test_wille_cannot_delete_skill(self):
        '''Tests seele users can delete exist skills'''
        self._test_permission('wille', 'delete', obj=self.skill, negative=True)


class ServicePermissionTestCase(TestCase):
    def setUp(self):
        self.users = dict(
                adam=PersonaFactory(role='adam'),
                seele=PersonaFactory(role='seele'),
                nerv=PersonaFactory(role='nerv'),
                children=PersonaFactory(role='children'),
                wille=PersonaFactory(role='wille'),
            )
        self.service = ServiceFactory()
        self.user = PersonaFactory()

    def _test_permission(self, role, perm, obj=None, negative=False):
        user = self.users.get(role)
        perm = "profiles.{}_service".format(perm)
        if negative:
            self.assertFalse(user.has_perm(perm, obj=obj),
                "{} should not have '{}'".format(role.capitalize(), perm))
        else:
            self.assertTrue(user.has_perm(perm, obj=obj),
                "{} should have '{}'".format(role.capitalize(), perm))

    def test_seele_can_add_service(self):
        '''Tests seele users can add new services'''
        self._test_permission('seele', 'add')

    def test_nerv_can_add_service(self):
        '''Tests seele users can add new services'''
        self._test_permission('nerv', 'add')

    def test_children_cannot_add_service(self):
        '''Tests seele users can add new services'''
        self._test_permission('children', 'add', negative=True)

    def test_wille_cannnot_add_service(self):
        '''Tests seele users can add new services'''
        self._test_permission('wille', 'add', negative=True)

    def test_seele_can_change_service(self):
        '''Tests seele users can change exist services'''
        self._test_permission('seele', 'change', obj=self.service)

    def test_nerv_can_change_service(self):
        '''Tests seele users can change exist services'''
        self._test_permission('nerv', 'change', obj=self.service)

    def test_children_cannot_change_service(self):
        '''Tests seele users can change exist services'''
        self._test_permission('children', 'change', obj=self.service, negative=True)

    def test_wille_cannot_change_service(self):
        '''Tests seele users can change exist services'''
        self._test_permission('wille', 'change', obj=self.service, negative=True)

    def test_seele_can_delete_service(self):
        '''Tests seele users can delete exist services'''
        self._test_permission('seele', 'delete', obj=self.service)

    def test_nerv_can_delete_service(self):
        '''Tests seele users can delete exist services'''
        self._test_permission('nerv', 'delete', obj=self.service)

    def test_children_cannot_delete_service(self):
        '''Tests seele users can delete exist services'''
        self._test_permission('children', 'delete', obj=self.service, negative=True)

    def test_wille_cannnot_delete_service(self):
        '''Tests seele users can delete exist services'''
        self._test_permission('wille', 'delete', obj=self.service, negative=True)