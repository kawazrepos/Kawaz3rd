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
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='Label', max_length=16, unique=True)),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order')),
            ],
            options={
                'verbose_name': 'Label',
                'verbose_name_plural': 'Label',
                'ordering': ('order',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('pub_state', models.CharField(verbose_name='Publish status', default='public', max_length=10, choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')])),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('body', models.TextField(verbose_name='Body')),
                ('period_start', models.DateTimeField(verbose_name='Start time', blank=True, null=True)),
                ('period_end', models.DateTimeField(verbose_name='End time', blank=True, null=True)),
                ('place', models.CharField(verbose_name='Place', blank=True, max_length=255)),
                ('number_restriction', models.PositiveIntegerField(verbose_name='Number restriction', blank=True, default=None, help_text='Use this to limit the number of attendees.', null=True)),
                ('attendance_deadline', models.DateTimeField(verbose_name='Attendance deadline', blank=True, default=None, help_text='A deadline of the attendance. No member can attend the event after this deadline.', null=True)),
                ('created_at', models.DateTimeField(verbose_name='Created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='Modified at', auto_now=True)),
                ('attendees', models.ManyToManyField(verbose_name='Attendees', editable=False, to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(verbose_name='Category', to='events.Category', blank=True, null=True)),
                ('organizer', models.ForeignKey(verbose_name='Organizer', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
                'ordering': ('period_start', 'period_end', '-created_at', '-updated_at', 'title', '-pk'),
                'permissions': (('attend_event', 'Can attend the event'), ('quit_event', 'Can quit the event'), ('view_event', 'Can view the event')),
            },
            bases=(models.Model,),
        ),
    ]
