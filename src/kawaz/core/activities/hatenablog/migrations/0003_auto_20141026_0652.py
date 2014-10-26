# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hatenablog', '0002_auto_20141014_2146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hatenablogentry',
            options={'ordering': ('-created_at',), 'verbose_name_plural': '広報ブログの記事', 'verbose_name': '広報ブログの記事'},
        ),
        migrations.AlterField(
            model_name='hatenablogentry',
            name='created_at',
            field=models.DateTimeField(verbose_name='作成日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hatenablogentry',
            name='title',
            field=models.CharField(max_length=128, verbose_name='タイトル'),
            preserve_default=True,
        ),
    ]
