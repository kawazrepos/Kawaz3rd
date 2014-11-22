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
                ('label', models.CharField(max_length=255, verbose_name='Category name')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='blog_categories', verbose_name='Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('pub_state', models.CharField(max_length=10, default='public', choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')], verbose_name='Publish status')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Body')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('publish_at', models.DateTimeField(editable=False, null=True, verbose_name='Published at')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, related_name='blog_entries', verbose_name='Author')),
                ('category', models.ForeignKey(to='blogs.Category', related_name='entries', null=True, blank=True, verbose_name='Category')),
            ],
            options={
                'permissions': (('view_entry', 'Can view the entry'),),
                'ordering': ('-updated_at', 'title'),
                'verbose_name_plural': 'Entries',
                'verbose_name': 'Entry',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('author', 'label')]),
        ),
    ]
