# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleCalendarBridge',
            fields=[
                ('event', models.OneToOneField(to='events.Event', primary_key=True, serialize=False)),
                ('gcal_event_id', models.CharField(default='', editable=False, max_length=128, blank=True, verbose_name='Google Calendar Event ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
