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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=128)),
                ('url', models.URLField(verbose_name='URL', unique=True)),
                ('thumbnail', models.ImageField(verbose_name='Image', upload_to=kawaz.apps.recent_activities.models.RecentActivity._get_upload_path)),
                ('publish_at', models.DateTimeField(verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'Recent Activity',
                'verbose_name_plural': 'Recent Activities',
                'ordering': ('-publish_at',),
            },
            bases=(models.Model,),
        ),
    ]
