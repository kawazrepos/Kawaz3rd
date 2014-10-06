# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = []
    operations = []

    if getattr(settings, 'TESTING'):
        # settings.TESTING is assigned in
        # kawaz.core.tests.runner.KawazDiscoverRunner
        operations.extend([
            migrations.CreateModel(
                name='SingleObjectPreviewMixinTestArticle',
                fields=[
                    ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                    ('foo', models.CharField(max_length=50, verbose_name='foo')),
                    ('foo', models.TextField(verbose_name='bar')),
                ],
                options={
                },
                bases=(models.Model,),
            ),
        ])
