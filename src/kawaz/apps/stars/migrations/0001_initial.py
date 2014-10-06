# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(verbose_name='Object ID')),
                ('quote', models.CharField(blank=True, verbose_name='Quote', help_text='This is used for quotation. When the user add a star with text selection, the selected text is passed to this.', max_length=512, default='')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Created at')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_star', to='contenttypes.ContentType', verbose_name='Content Type')),
            ],
            options={
                'ordering': ('created_at',),
                'verbose_name_plural': 'Stars',
                'permissions': (('view_star', 'Can view the Star'),),
                'verbose_name': 'Star',
            },
            bases=(models.Model,),
        ),
    ]

    if getattr(settings, 'TESTING'):
        # settings.TESTING is assigned in
        # kawaz.core.tests.runner.KawazDiscoverRunner
        operations.extend([
            migrations.CreateModel(
                name='StarTestArticle',
                fields=[
                    ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                    ('pub_state', models.CharField(default='public', max_length=10, choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')], verbose_name='Publish status')),
                    ('title', models.CharField(max_length=255, verbose_name='Title')),
                    ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ],
                options={
                },
                bases=(models.Model,),
            ),
        ])
