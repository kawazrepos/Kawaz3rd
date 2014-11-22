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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('pub_state', models.CharField(choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')], verbose_name='Publish status', max_length=10, default='public')),
                ('title', models.CharField(verbose_name='Title', max_length=128)),
                ('body', models.TextField(verbose_name='Body')),
                ('created_at', models.DateTimeField(verbose_name='Created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='Modified at', auto_now=True)),
                ('author', models.ForeignKey(related_name='created_announcements', editable=False, to=settings.AUTH_USER_MODEL)),
                ('last_modifier', models.ForeignKey(verbose_name='Last modified by', related_name='last_modified_announcements', null=True, editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Announcement',
                'verbose_name_plural': 'Announcements',
                'permissions': (('view_announcement', 'Can view the announcement'),),
                'ordering': ('-created_at',),
            },
            bases=(models.Model,),
        ),
    ]
