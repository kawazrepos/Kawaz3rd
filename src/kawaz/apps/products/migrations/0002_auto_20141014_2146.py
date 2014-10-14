# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kawaz.apps.products.models
import thumbnailfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='order',
            field=models.PositiveSmallIntegerField(verbose_name='並び変え', help_text='この値が小さい順に並びます', default=0),
        ),
        migrations.AlterField(
            model_name='packagerelease',
            name='file_content',
            field=models.FileField(verbose_name='ファイル', upload_to=kawaz.apps.products.models.PackageRelease._get_upload_path),
        ),
        migrations.AlterField(
            model_name='platform',
            name='order',
            field=models.PositiveSmallIntegerField(verbose_name='並び変え', help_text='この値が小さい順に並びます', default=0),
        ),
        migrations.AlterField(
            model_name='screenshot',
            name='image',
            field=thumbnailfield.fields.ThumbnailField(verbose_name='画像', upload_to=kawaz.apps.products.models.Screenshot._get_upload_path),
        ),
    ]
