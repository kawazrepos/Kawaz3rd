from django.test import TestCase
from .factories import ProfileFactory, AccountFactory, ServiceFactory, SkillFactory

class ProfileTestCase(TestCase):
    def test_create_user(self):
        """Tests can access profile via user.get_profile()"""
        profile = ProfileFactory()
        self.assertEqual(profile.user.get_profile(), profile)

class SkillTestCase(TestCase):
    def test_unicode(self):
        """Tests __unicode__ returns correct value"""
        skill = SkillFactory()
        self.assertEqual(skill.__unicode__(), skill.label)

class ServiceTestCase(TestCase):
    def test_unicode(self):
        """Tests __unicode__ returns correct value"""
        service = ServiceFactory()
        self.assertEqual(service.__unicode__(), service.label)

class AccountTestCase(TestCase):
    def test_get_url(self):
        """Tests can get URL from property"""
        account = AccountFactory(username='kawaz_tan')
        self.assertEqual(account.url, 'http://twitter.com/kawaz_tan/')

    def test_unicode(self):
        """Tests __unicode__ returns correct value"""
        account = AccountFactory(username='kawaz_tan')
        self.assertEqual(account.__unicode__(), '%s (%s @ %s)' % (account.username, account.user.username, account.service.label))
