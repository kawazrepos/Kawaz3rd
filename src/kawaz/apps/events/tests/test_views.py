from django.test import TestCase
from .factories import EventFactory
from kawaz.core.personas.tests.factories import PersonaFactory

class EventDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_user_can_view_public_event(self):
        '''Tests anonymous user can view public event'''
        event = EventFactory()
        r = self.client.get(event.get_absolute_url())
        self.assertTemplateUsed(r, 'events/event_detail.html')
        self.assertEqual(r.context_data['object'], event)

    def test_authorized_user_can_view_public_event(self):
        '''Tests authorized user can view public event'''
        event = EventFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(event.get_absolute_url())
        self.assertTemplateUsed(r, 'events/event_detail.html')
        self.assertEqual(r.context_data['object'], event)

    def test_anonymous_user_can_not_view_protected_event(self):
        '''Tests anonymous user can not view protected event'''
        event = EventFactory(pub_state='protected')
        r = self.client.get(event.get_absolute_url())
        self.assertEqual(r.status_code, 302) # ToDo check redirects after implement inspectional_registration

    def test_authorized_user_can_view_protected_event(self):
        '''Tests authorized user can view public event'''
        event = EventFactory(pub_state='protected')
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(event.get_absolute_url())
        self.assertTemplateUsed(r, 'events/event_detail.html')
        self.assertEqual(r.context_data['object'], event)

    def test_anonymous_user_can_not_view_draft_event(self):
        '''Tests anonymous user can not view draft event'''
        event = EventFactory(pub_state='draft')
        r = self.client.get(event.get_absolute_url())
        self.assertEqual(r.status_code, 302) # ToDo check redirects after implement inspectional_registration

    def test_others_can_not_view_draft_event(self):
        '''Tests others can not view draft event'''
        event = EventFactory(pub_state='draft')
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(event.get_absolute_url())
        self.assertEqual(r.status_code, 302) # ToDo check redirects after implement inspectional_registration

    def test_organizer_can_view_draft_event(self):
        '''Tests organizer can view draft event on update view'''
        event = EventFactory(pub_state='draft', organizer=self.user)
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(event.get_absolute_url())
        self.assertTemplateUsed(r, 'events/event_form.html')
        self.assertEqual(r.context_data['object'], event)
