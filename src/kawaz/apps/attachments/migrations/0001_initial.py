# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kawaz.apps.attachments.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('content_file', models.FileField(upload_to=kawaz.apps.attachments.models.Material._get_upload_path, verbose_name='Content file')),
                ('slug', models.SlugField(editable=False, unique=True, blank=True, verbose_name='Slug')),
                ('ip_address', models.IPAddressField(editable=False, verbose_name='IP Address')),
                ('created_at', models.DateTimeField(verbose_name='Created at', auto_now_add=True)),
                ('author', models.ForeignKey(verbose_name='Author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materials',
                'ordering': ('created_at',),
            },
            bases=(models.Model,),
        ),
    ]
