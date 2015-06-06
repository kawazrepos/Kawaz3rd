# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0003_auto_20150426_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='service',
            field=models.ForeignKey(to='personas.Service', related_name='accounts', verbose_name='Service'),
        ),
    ]
