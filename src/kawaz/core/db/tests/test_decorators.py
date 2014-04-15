from django.test import TestCase
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import EvenNumberContainer
from ..decorators import validate_on_save

class DecoratorsTestCase(TestCase):
    def test_validate_on_save(self):
        '''Tests @validate_on_save decorator works correctly'''
        self.assertIsNotNone(EvenNumberContainer.objects.create(number=1))

        setattr(settings, 'VALIDATE_ON_SAVE', True)
        DecoratedEvenNumberContainer = validate_on_save(EvenNumberContainer)()
        obj = DecoratedEvenNumberContainer.objects.create()
        obj.number = 2
        obj.save()

        def create():
            obj.number = 1
            obj.save()
        self.assertRaises(ValidationError, create)

    def test_validate_on_save_global_setting(self):
        '''Tests when settings.VALIDATE_ON_SAVE = False, @validate_on_save decorator doesn't work'''
        setattr(settings, 'VALIDATE_ON_SAVE', False)
        DecoratedEvenNumberContainer = validate_on_save(EvenNumberContainer)()
        obj = DecoratedEvenNumberContainer.objects.create(number=1)
        obj.save()

    def test_validate_on_save_force_update(self):
        '''Tests when force_update = True, validation is not available'''
        DecoratedEvenNumberContainer = validate_on_save(EvenNumberContainer)()
        obj = DecoratedEvenNumberContainer.objects.create(number=1)
        obj.save(force_update=True)
