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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('place', models.CharField(verbose_name='Place', max_length=64, help_text='Fill your address. You must be related with Sapporo or neighbor cities.')),
                ('skill', models.TextField(verbose_name='Skill', max_length=2048, help_text='Fill your skills or what you want to do which related to game development.')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='Remarks')),
                ('registration_profile', models.OneToOneField(to='registration.RegistrationProfile', verbose_name='registration profile', editable=False, related_name='_supplement')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
