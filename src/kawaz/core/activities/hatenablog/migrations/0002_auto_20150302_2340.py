# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kawaz.core.files.storages
import kawaz.core.activities.hatenablog.models


class Migration(migrations.Migration):

    dependencies = [
        ('hatenablog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hatenablogentry',
            name='thumbnail',
            field=models.ImageField(upload_to=kawaz.core.activities.hatenablog.models.HatenablogEntry._get_upload_path, storage=kawaz.core.files.storages.OverwriteStorage(), verbose_name='Image', default=''),
            preserve_default=True,
        ),
    ]
