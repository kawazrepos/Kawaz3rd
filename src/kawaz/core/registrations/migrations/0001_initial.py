# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationSupplement',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('place', models.CharField(max_length=64, verbose_name='Place', help_text='Fill your address. You must be related with Sapporo or neighbor cities.')),
                ('skill', models.TextField(max_length=2048, verbose_name='Skill', help_text='Fill your skills or what you want to do which related to game development.')),
                ('remarks', models.TextField(null=True, verbose_name='Remarks', blank=True)),
                ('registration_profile', models.OneToOneField(related_name='_supplement', verbose_name='registration profile', to='registration.RegistrationProfile', editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
