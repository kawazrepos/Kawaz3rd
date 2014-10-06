# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('pub_state', models.CharField(default='public', max_length=10, choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')], verbose_name='Publish status')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Body')),
                ('created_at', models.DateTimeField(verbose_name='Created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='Modified at', auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_announcements', editable=False)),
            ],
            options={
                'ordering': ('-created_at',),
                'permissions': (('view_announcement', 'Can view the announcement'),),
                'verbose_name_plural': 'Announcements',
                'verbose_name': 'Announcement',
            },
            bases=(models.Model,),
        ),
    ]
