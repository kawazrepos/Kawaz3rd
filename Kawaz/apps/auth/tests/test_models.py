from django.test import TestCase

class UserTestCase(TestCase):
    def test_can_run_test(self):
        """Tests"""
        self.assertEqual(1 + 1, 2)
