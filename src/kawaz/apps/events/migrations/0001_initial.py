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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('label', models.CharField(unique=True, verbose_name='Label', max_length=16)),
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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('pub_state', models.CharField(verbose_name='Publish status', default='public', choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')], max_length=10)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('body', models.TextField(verbose_name='Body')),
                ('period_start', models.DateTimeField(verbose_name='Start time', blank=True, null=True)),
                ('period_end', models.DateTimeField(verbose_name='End time', blank=True, null=True)),
                ('place', models.CharField(verbose_name='Place', blank=True, max_length=255)),
                ('number_restriction', models.PositiveIntegerField(verbose_name='Number restriction', help_text='Use this to limit the number of attendees.', default=None, blank=True, null=True)),
                ('attendance_deadline', models.DateTimeField(verbose_name='Attendance deadline', help_text='A deadline of the attendance. No member can attend the event after this deadline.', default=None, blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('attendees', models.ManyToManyField(related_name='events_attend', verbose_name='Attendees', to=settings.AUTH_USER_MODEL, editable=False)),
                ('category', models.ForeignKey(verbose_name='Category', to='events.Category', blank=True, null=True)),
                ('organizer', models.ForeignKey(related_name='events_owned', verbose_name='Organizer', to=settings.AUTH_USER_MODEL, editable=False, null=True)),
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
