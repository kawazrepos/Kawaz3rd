# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20141123_0104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='platforms',
            field=models.ManyToManyField(to='products.Platform', verbose_name='Platforms', related_name='products'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='published_at',
            field=models.DateField(help_text='If this product have been already released, please fill the date.', verbose_name='Published at'),
            preserve_default=True,
        ),
    ]
