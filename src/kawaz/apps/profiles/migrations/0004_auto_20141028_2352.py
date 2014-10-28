# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20141026_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pub_state',
            field=models.CharField(choices=[('public', '外部公開'), ('protected', '内部公開')], verbose_name='公開設定', max_length=10, default='public'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='place',
            field=models.CharField(blank=True, verbose_name='住んでるところ', max_length=255),
            preserve_default=True,
        ),
    ]
