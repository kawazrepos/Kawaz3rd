# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kawaz.apps.recent_activities.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecentActivity',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('url', models.URLField(verbose_name='URL', unique=True)),
                ('thumbnail', models.ImageField(upload_to=kawaz.apps.recent_activities.models.RecentActivity._get_upload_path, verbose_name='Image')),
                ('publish_at', models.DateTimeField(verbose_name='Created at')),
            ],
            options={
                'ordering': ('-publish_at',),
                'verbose_name': 'Recent Activity',
                'verbose_name_plural': 'Recent Activities',
            },
            bases=(models.Model,),
        ),
    ]
