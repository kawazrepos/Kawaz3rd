# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(verbose_name='Attendees', to=settings.AUTH_USER_MODEL, related_name='events_attend'),
            preserve_default=True,
        ),
    ]
