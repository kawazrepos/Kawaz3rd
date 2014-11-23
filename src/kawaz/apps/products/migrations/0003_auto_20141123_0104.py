# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20141115_1411'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'ordering': ('display_mode', '-published_at'), 'permissions': (('join_product', 'Can join to the product'), ('quit_product', 'Can quit from the product')), 'verbose_name_plural': 'Products'},
        ),
        migrations.RenameField(
            model_name='product',
            old_name='publish_at',
            new_name='published_at',
        ),
        migrations.AlterField(
            model_name='product',
            name='contact_info',
            field=models.CharField(max_length=256, verbose_name='Contact info', blank=True, help_text='Fill your contact info for visitors, e.g. Twitter account, Email address or Facebook account', default=''),
            preserve_default=True,
        ),
    ]
