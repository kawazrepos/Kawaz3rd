# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='contact_info',
            field=models.TextField(help_text='Fill your contact info for visitors, e.f. Twitter account, Email address or Facebook account', default='', verbose_name='Contact info', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='packagerelease',
            name='version',
            field=models.CharField(max_length=32, default='', blank=True, verbose_name='Version'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlrelease',
            name='version',
            field=models.CharField(max_length=32, default='', blank=True, verbose_name='Version'),
            preserve_default=True,
        ),
    ]
