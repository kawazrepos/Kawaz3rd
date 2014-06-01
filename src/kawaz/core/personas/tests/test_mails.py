from django.test import TestCase
from django.template.loader import render_to_string

class PersonaPasswordResetMailTemplateTestCase(TestCase):
    def test_email_subject_parse(self):
        """
        registration/password_reset_email_subject.txtを正しくparseできる
        """
        rendered = render_to_string('registration/password_reset_subject.txt')
        self.assertIsNotNone(rendered)

    def test_email_parse(self):
        """
        registration/password_reset_email.htmlを正しくparseできる
        """
        rendered = render_to_string('registration/password_reset_email.html')
        self.assertIsNotNone(rendered)

