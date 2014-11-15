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
            field=models.CharField(help_text='Fill your contact info for visitors, e.f. Twitter account, Email address or Facebook account', blank=True, default='', max_length=256, verbose_name='Contact info'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='packagerelease',
            name='version',
            field=models.CharField(verbose_name='Version', blank=True, default='', max_length=32),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlrelease',
            name='version',
            field=models.CharField(verbose_name='Version', blank=True, default='', max_length=32),
            preserve_default=True,
        ),
    ]
