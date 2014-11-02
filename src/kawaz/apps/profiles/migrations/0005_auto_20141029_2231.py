# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20141028_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='place',
            field=models.CharField(verbose_name='住んでいるところ', blank=True, max_length=255),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='service',
            name='url_pattern',
            field=models.CharField(verbose_name='URLパターン', blank=True, null=True, max_length=256),
            preserve_default=True,
        ),
    ]
