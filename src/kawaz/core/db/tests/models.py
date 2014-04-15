from django.core.exceptions import ValidationError
from django.db import models

class EvenNumberContainer(models.Model):
    number = models.IntegerField('number', default=0)

    class Meta:
        app_label = 'db'

    def clean(self):
        if self.number % 2 == 1:
            raise ValidationError('number must be even')
        super(EvenNumberContainer, self).clean()
