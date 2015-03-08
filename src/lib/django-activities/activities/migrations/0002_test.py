# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activities', '0001_initial'),
    ]

    operations = []

    if getattr(settings, 'TESTING'):
        # settings.TESTING is assigned in
        # kawaz.core.tests.runner.KawazDiscoverRunner
        operations.extend([
            migrations.CreateModel(
                name='ActivitiesTestModelA',
                fields=[
                    ('id', models.AutoField(
                        auto_created=True, serialize=False,
                        primary_key=True, verbose_name='ID')),
                    ('text', models.CharField(
                        max_length=255, verbose_name='Text')),
                ],
                options={
                },
                bases=(models.Model,),
            ),
            migrations.CreateModel(
                name='ActivitiesTestModelB',
                fields=[
                    ('id', models.AutoField(
                        auto_created=True, serialize=False,
                        primary_key=True, verbose_name='ID')),
                    ('text', models.CharField(
                        max_length=255, verbose_name='Text')),
                ],
                options={
                },
                bases=(models.Model,),
            ),
            migrations.CreateModel(
                name='ActivitiesTestModelC',
                fields=[
                    ('id', models.AutoField(
                        auto_created=True, serialize=False,
                        primary_key=True, verbose_name='ID')),
                    ('text', models.CharField(
                        max_length=255, verbose_name='Text')),
                ],
                options={
                },
                bases=(models.Model,),
            ),
        ])
