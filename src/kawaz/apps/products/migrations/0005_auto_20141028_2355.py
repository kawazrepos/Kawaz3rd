# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import thumbnailfield.fields
import kawaz.apps.products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20141026_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='advertisement_image',
            field=thumbnailfield.fields.ThumbnailField(help_text='This would be used in the top page. The aspect ratio of the image should be 16:9We recommend the image size to be 800 * 450', upload_to=kawaz.apps.products.models.Product._get_advertisement_image_upload_path, verbose_name='告知用画像', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='display_mode',
            field=models.CharField(help_text="How the product displayed on the top page. To use 'Featured', an 'Advertisement image' is required.", max_length=10, verbose_name='表示モード', choices=[('featured', 'Fetured: Displayed in the curled cell and the tiled cell on the top page'), ('tiled', 'Tiled: Displayed in the tiled cell on the top page'), ('normal', 'Normal: Displayed only in tiled cell on the detailed page')], default='normal'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='project',
            field=models.OneToOneField(null=True, verbose_name='プロジェクト', related_name='product', to='projects.Project', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=thumbnailfield.fields.ThumbnailField(help_text='This would be used as a product thumbnail image. The aspect ratio of the image should be 16:9.We recommend the image size to be 800 * 450.', upload_to=kawaz.apps.products.models.Product._get_thumbnail_upload_path, verbose_name='サムネイル'),
            preserve_default=True,
        ),
    ]
