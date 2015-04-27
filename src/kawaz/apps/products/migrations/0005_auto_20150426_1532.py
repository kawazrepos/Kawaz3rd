# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kawaz.apps.products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20141203_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packagerelease',
            name='product',
            field=kawaz.apps.products.models.UnsavedForeignKey(verbose_name='Product', editable=False, related_name='packagereleases', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='screenshot',
            name='product',
            field=kawaz.apps.products.models.UnsavedForeignKey(verbose_name='Product', editable=False, related_name='screenshots', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='urlrelease',
            name='product',
            field=kawaz.apps.products.models.UnsavedForeignKey(verbose_name='Product', editable=False, related_name='urlreleases', to='products.Product'),
        ),
    ]
