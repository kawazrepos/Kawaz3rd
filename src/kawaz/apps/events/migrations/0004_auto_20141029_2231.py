# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20141026_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='attendance_deadline',
            field=models.DateTimeField(help_text='参加締切日。この日時を過ぎた場合、参加することはできません', verbose_name='参加締切日', blank=True, default=None, null=True),
            preserve_default=True,
        ),
    ]
