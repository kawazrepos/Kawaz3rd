# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kawaz.core.activities.hatenablog.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HatenablogEntry',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('url', models.URLField(verbose_name='URL', unique=True)),
                ('thumbnail', models.ImageField(upload_to=kawaz.core.activities.hatenablog.models.HatenablogEntry._get_upload_path, default='', verbose_name='Image')),
                ('md5', models.CharField(max_length=32)),
                ('created_at', models.DateTimeField(verbose_name='Created at')),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name_plural': 'Hatenablog entries',
                'verbose_name': 'Hatenablog entry',
            },
            bases=(models.Model,),
        ),
    ]
