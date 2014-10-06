# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleCalendarBridge',
            fields=[
                ('event', models.OneToOneField(serialize=False, to='events.Event', primary_key=True)),
                ('gcal_event_id', models.CharField(blank=True, editable=False, max_length=128, default='', verbose_name='Google Calendar Event ID')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
