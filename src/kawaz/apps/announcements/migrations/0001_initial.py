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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('pub_state', models.CharField(verbose_name='Publish status', default='public', max_length=10, choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')])),
                ('title', models.CharField(verbose_name='Title', max_length=128)),
                ('body', models.TextField(verbose_name='Body')),
                ('silently', models.BooleanField(verbose_name='Silently', default=False, help_text='If you checked this field. This will not be notified anybody.')),
                ('created_at', models.DateTimeField(verbose_name='Created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='Modified at', auto_now=True)),
                ('author', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
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
