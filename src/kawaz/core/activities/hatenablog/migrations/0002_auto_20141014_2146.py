# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hatenablog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hatenablogentry',
            name='md5',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hatenablogentry',
            name='created_at',
            field=models.DateTimeField(verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='hatenablogentry',
            name='title',
            field=models.CharField(verbose_name='Title', max_length=128),
        ),
    ]
