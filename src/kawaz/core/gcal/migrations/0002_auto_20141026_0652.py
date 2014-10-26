# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gcal', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='googlecalendarbridge',
            name='gcal_event_id',
            field=models.CharField(max_length=128, default='', blank=True, editable=False, verbose_name='GoogleカレンダーのイベントID'),
            preserve_default=True,
        ),
    ]
