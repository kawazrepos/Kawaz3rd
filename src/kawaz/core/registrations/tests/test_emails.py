from django.test import TestCase, override_settings
from django.template import Context
from django.template.loader import render_to_string


@override_settings(GEEKDRUMS_NAME='geekdrums')
class RegistrationMailTemplateTestCase(TestCase):
    def test_acceptance_subject_parse(self):
        """
        registration/acceptance_email_subject.txtを正しくparseできる
        """
        rendered = render_to_string('registration/acceptance_email_subject.txt')
        self.assertIsNotNone(rendered)

    def test_acceptance_parse(self):
        """
        registration/acceptance_email.txtを正しくparseできる
        """
        context = Context(dict(
            activation_key='thisisanactivationkey',
        ))
        rendered = render_to_string(
            'registration/acceptance_email.txt',
            context_instance=context,
        )
        self.assertIsNotNone(rendered)
        self.assertIn('geekdrums', rendered)

    def test_rejection_subject_parse(self):
        """
        registration/rejection_email_subject.txtを正しくparseできる
        """
        rendered = render_to_string('registration/rejection_email_subject.txt')
        self.assertIsNotNone(rendered)

    def test_rejection_parse(self):
        """
        registration/rejection_email.txtを正しくparseできる
        """
        rendered = render_to_string('registration/rejection_email.txt')
        self.assertIsNotNone(rendered)
        self.assertIn('geekdrums', rendered)

    def test_registration_subject_parse(self):
        """
        registration/registration_email_subject.txtを正しくparseできる
        """
        rendered = render_to_string('registration/registration_email_subject.txt')
        self.assertIsNotNone(rendered)

    def test_registration_parse(self):
        """
        registration/registration_email.txtを正しくparseできる
        """
        rendered = render_to_string('registration/registration_email.txt')
        self.assertIsNotNone(rendered)
        self.assertIn('geekdrums', rendered)


    def test_registration_subject_parse(self):
        """
        registration/registration_email_subject.txtを正しくparseできる
        """
        rendered = render_to_string('registration/registration_email_subject.txt')
        self.assertIsNotNone(rendered)

    def test_registration_parse(self):
        """
        registration/registration_email.txtを正しくparseできる
        """
        rendered = render_to_string('registration/registration_email.txt')
        self.assertIsNotNone(rendered)
        self.assertIn('geekdrums', rendered)

    def test_notification_subject_parse(self):
        """
        registration/notification_email_subject.txtを正しくparseできる
        """
        rendered = render_to_string('registration/notification_email_subject.txt')
        self.assertIsNotNone(rendered)

    def test_notification_parse(self):
        """
        registration/notification_email.txtを正しくparseできる
        """
        rendered = render_to_string('registration/notification_email.txt')
        self.assertIsNotNone(rendered)
        self.assertIn('geekdrums', rendered)


