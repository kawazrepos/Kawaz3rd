# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kawaz.apps.attachments.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='material',
            options={'ordering': ('created_at',), 'verbose_name_plural': '素材', 'verbose_name': '素材'},
        ),
        migrations.AlterField(
            model_name='material',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='作者'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='content_file',
            field=models.FileField(upload_to=kawaz.apps.attachments.models.Material._get_upload_path, verbose_name='ファイル'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='material',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='素材ID', editable=False, unique=True),
            preserve_default=True,
        ),
    ]
