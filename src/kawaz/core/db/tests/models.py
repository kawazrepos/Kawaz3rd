from django.db import models
from django.core.exceptions import ValidationError


class EvenNumberContainer(models.Model):
    """A test model which does not allow to store odd number"""
    number = models.IntegerField('number', default=0)

    class Meta:
        app_label = 'db'

    def clean(self):
        if self.number % 2 == 1:
            raise ValidationError('number must be even')
