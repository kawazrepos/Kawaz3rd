from unittest.mock import MagicMock
from django.template import Context
from django.test import TestCase
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode


class PersonaPasswordResetMailTemplateTestCase(TestCase):
    def test_email_subject_parse(self):
        """
        registration/password_reset_email_subject.txtを正しくparseできる
        """
        rendered = render_to_string('registration/password_reset_subject.txt')
        self.assertTrue(rendered != '')

    def test_email_parse(self):
        """
        registration/password_reset_email.htmlを正しくparseできる
        """
        user = MagicMock()
        c = Context({
            'email': 'webmaster@kawaz.org',
            'domain': 'www.kawaz.org',
            'site_name': 'Kawaz',
            'uid': urlsafe_base64_encode(1),
            'user': user,
            'token': "hogehogehogehoge",
            'protocol': 'http',
        })
        rendered = render_to_string('registration/password_reset_email.html', c)
        self.assertTrue(rendered != '')

