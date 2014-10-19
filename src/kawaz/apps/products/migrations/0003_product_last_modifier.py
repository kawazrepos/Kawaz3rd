# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_auto_20141014_2146'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='last_modifier',
            field=models.ForeignKey(verbose_name='Last modified by', related_name='last_modified_products', editable=False, null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
