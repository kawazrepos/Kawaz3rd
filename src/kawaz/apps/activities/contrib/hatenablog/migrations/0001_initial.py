# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kawaz.apps.activities.contrib.hatenablog.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HatenablogEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='タイトル', max_length=128)),
                ('url', models.URLField(verbose_name='URL', unique=True)),
                ('thumbnail', models.ImageField(verbose_name='画像', upload_to=kawaz.apps.activities.contrib.hatenablog.models.HatenablogEntry._get_upload_path, default='')),
                ('created_at', models.DateTimeField(verbose_name='作成日時')),
            ],
            options={
                'verbose_name': 'Hatenablog entry',
                'verbose_name_plural': 'Hatenablog entries',
                'ordering': ('-created_at',),
            },
            bases=(models.Model,),
        ),
    ]
