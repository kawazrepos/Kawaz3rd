from unittest.mock import MagicMock
from django.test import TestCase
from django.conf import settings
from django.test.utils import override_settings
from django.core.exceptions import ValidationError

from .models import EvenNumberContainer
from ..decorators import validate_on_save

class ValidationOnSaveDecoratorTestCase(TestCase):
    def test_non_validate_on_save(self):
        """`full_clean` method should not be called without validate_on_save decorator"""
        # escape original full_clean method
        original_full_clean = EvenNumberContainer.full_clean
        # set mock method
        EvenNumberContainer.full_clean = MagicMock(wraps=original_full_clean)

        # object create should finish without any exception because it is even
        self.assertIsNotNone(EvenNumberContainer.objects.create(number=2))

        # make sure that full_clean is not called
        self.assertFalse(EvenNumberContainer.full_clean.called)

        # object create should finish without any exception even the number is
        # odd because `full_clean` is not called
        self.assertIsNotNone(EvenNumberContainer.objects.create(number=1))

        # make sure that full_clean is not called
        self.assertFalse(EvenNumberContainer.full_clean.called)


    def test_validate_on_save(self):
        """`full_clean` method should be called with validate_on_save decorator"""
        # decorate the class
        DecoratedEvenNumberContainer = validate_on_save(EvenNumberContainer)

        # escape original full_clean method
        original_full_clean = DecoratedEvenNumberContainer.full_clean
        # set mock method
        DecoratedEvenNumberContainer.full_clean = MagicMock(wraps=original_full_clean)

        # object create should finish without any exception because it is even
        self.assertIsNotNone(DecoratedEvenNumberContainer.objects.create(number=2))

        # make sure that full_clean is called
        self.assertTrue(DecoratedEvenNumberContainer.full_clean.called)

        # object create should raise ValidationError because the number is odd
        self.assertRaises(ValidationError,
                          DecoratedEvenNumberContainer.objects.create,
                          number=1)

        # make sure that full_clean is called twice
        self.assertEqual(DecoratedEvenNumberContainer.full_clean.call_count, 2)


    @override_settings(
        VALIDATE_ON_SAVE_DISABLE=True,
    )
    def test_validate_on_save_disabled(self):
        """`full_clean` method should not be called with VALIDATE_ON_SAVE_DISABLE"""
        # decorate the class
        DecoratedEvenNumberContainer = validate_on_save(EvenNumberContainer)

        # escape original full_clean method
        original_full_clean = DecoratedEvenNumberContainer.full_clean
        # set mock method
        DecoratedEvenNumberContainer.full_clean = MagicMock(wraps=original_full_clean)

        # object create should finish without any exception because it is even
        self.assertIsNotNone(DecoratedEvenNumberContainer.objects.create(number=2))

        # make sure that full_clean is not called
        self.assertFalse(EvenNumberContainer.full_clean.called)

        # object create should finish without any exception even the number is
        # odd because VALIDATE_ON_SAVE_DISABLE=True
        self.assertIsNotNone(DecoratedEvenNumberContainer.objects.create(number=1))

        # make sure that full_clean is not called
        self.assertFalse(EvenNumberContainer.full_clean.called)
