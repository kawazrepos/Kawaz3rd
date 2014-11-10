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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('label', models.CharField(max_length=16, verbose_name='Label', unique=True)),
                ('order', models.PositiveSmallIntegerField(verbose_name='Order')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name_plural': 'Label',
                'verbose_name': 'Label',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('pub_state', models.CharField(max_length=10, default='public', choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')], verbose_name='Publish status')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Body')),
                ('period_start', models.DateTimeField(null=True, blank=True, verbose_name='Start time')),
                ('period_end', models.DateTimeField(null=True, blank=True, verbose_name='End time')),
                ('place', models.CharField(max_length=255, blank=True, verbose_name='Place')),
                ('number_restriction', models.PositiveIntegerField(blank=True, null=True, default=None, help_text='Use this to limit the number of attendees.', verbose_name='Number restriction')),
                ('attendance_deadline', models.DateTimeField(blank=True, null=True, default=None, help_text='A deadline of the attendance. No member can attend the event after this deadline.', verbose_name='Attendance deadline')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('attendees', models.ManyToManyField(to=settings.AUTH_USER_MODEL, editable=False, related_name='events_attend', verbose_name='Attendees')),
                ('category', models.ForeignKey(to='events.Category', null=True, blank=True, verbose_name='Category')),
                ('organizer', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, related_name='events_owned', null=True, verbose_name='Organizer')),
            ],
            options={
                'permissions': (('attend_event', 'Can attend the event'), ('quit_event', 'Can quit the event'), ('view_event', 'Can view the event')),
                'ordering': ('period_start', 'period_end', '-created_at', '-updated_at', 'title', '-pk'),
                'verbose_name_plural': 'Events',
                'verbose_name': 'Event',
            },
            bases=(models.Model,),
        ),
    ]
