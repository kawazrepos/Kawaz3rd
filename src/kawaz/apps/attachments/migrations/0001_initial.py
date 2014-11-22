# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import kawaz.apps.attachments.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('content_file', models.FileField(upload_to=kawaz.apps.attachments.models.Material._get_upload_path, verbose_name='Content file')),
                ('slug', models.SlugField(editable=False, blank=True, unique=True, verbose_name='Material slug')),
                ('ip_address', models.IPAddressField(editable=False, verbose_name='IP Address')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'ordering': ('created_at',),
                'verbose_name_plural': 'Materials',
                'verbose_name': 'Material',
            },
            bases=(models.Model,),
        ),
    ]
