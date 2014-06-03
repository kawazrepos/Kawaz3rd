from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from django.contrib.auth.models import AnonymousUser
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Announcement
from .factories import AnnouncementFactory


class AnnouncementsTemplateTagTestCase(TestCase):
    def setUp(self):
        self.announcements = dict(
            public=AnnouncementFactory(pub_state='public'),
            protected=AnnouncementFactory(pub_state='protected'),
            draft=AnnouncementFactory(pub_state='draft'),
        )

    def test_get_announcements(self):
        """get_announcements should put public and protected announcements"""
        t = Template(
            "{% load announcements_tags %}"
            "{% get_announcements as announcements %}"
        )
        c = Context({})
        t.render(c)
        self.assertEqual(c['announcements'].count(), 2)
        self.assertEqual(
            c['announcements'].filter(pub_state='draft').count(), 0)

    def test_get_announcements_with_public(self):
        """get_announcements should put public announcements"""
        t = Template(
            "{% load announcements_tags %}"
            "{% get_announcements 'public' as announcements %}"
        )
        c = Context({})
        t.render(c)
        self.assertEqual(c['announcements'].count(), 1)
        self.assertEqual(c['announcements'].first(),
                         self.announcements['public'])

    def test_get_announcements_with_protected(self):
        """get_announcements should put protected announcements"""
        t = Template(
            "{% load announcements_tags %}"
            "{% get_announcements 'protected' as announcements %}"
        )
        c = Context({})
        t.render(c)
        self.assertEqual(c['announcements'].count(), 1)
        self.assertEqual(c['announcements'].first(),
                         self.announcements['protected'])

    def test_get_announcements_with_draft(self):
        """get_announcements should put draft announcements"""
        t = Template(
            "{% load announcements_tags %}"
            "{% get_announcements 'draft' as announcements %}"
        )
        c = Context({})
        t.render(c)
        self.assertEqual(c['announcements'].count(), 1)
        self.assertEqual(c['announcements'].first(),
                         self.announcements['draft'])

    def test_get_announcements_with_unknown(self):
        """get_announcements should raise TemplateSyntaxError"""
        t = Template(
            "{% load announcements_tags %}"
            "{% get_announcements 'unknown' as announcements %}"
        )
        c = Context({})
        self.assertRaises(TemplateSyntaxError,
                          t.render, c)




