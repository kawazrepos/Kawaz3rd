# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0002_auto_20141026_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='slug',
            field=models.SlugField(unique=True, blank=True, editable=False, verbose_name='Material slug'),
            preserve_default=True,
        ),
    ]
