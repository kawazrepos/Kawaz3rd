# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='gender',
            field=models.CharField(verbose_name='Gender', choices=[('man', 'Man'), ('woman', 'Woman'), ('unknown', '不明')], default='unknown', max_length=10),
        ),
    ]
