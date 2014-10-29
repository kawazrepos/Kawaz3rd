# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0003_auto_20141028_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='slug',
            field=models.SlugField(verbose_name='素材ID', blank=True, unique=True, editable=False),
            preserve_default=True,
        ),
    ]
