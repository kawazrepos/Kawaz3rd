# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = []

    if getattr(settings, 'TESTING'):
        # settings.TESTING is assigned in
        # kawaz.core.tests.runner.KawazDiscoverRunner
        operations.extend([
            migrations.CreateModel(
                name='PublishmentTestArticle',
                fields=[
                    ('id', models.AutoField(
                        auto_created=True, serialize=False,
                        primary_key=True, verbose_name='ID')),
                    ('pub_state', models.CharField(
                        default='public', max_length=10,
                        choices=[
                            ('public', 'Public'),
                            ('protected', 'Internal'), 
                            ('draft', 'Draft')
                        ], verbose_name='Publish status')),
                    ('title', models.CharField(
                        max_length=255, verbose_name='Title')),
                    ('author', models.ForeignKey(
                        to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ],
                options={
                },
                bases=(models.Model,),
            ),
            migrations.AlterModelOptions(
                name='PublishmentTestArticle',
                options={'permissions': (('view_publishmenttestarticle', 'Can view the articles'),)},
            ),
        ])
