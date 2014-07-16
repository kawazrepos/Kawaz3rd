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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('label', models.CharField(max_length=255, verbose_name='Category name')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('author', 'label')]),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('pub_state', models.CharField(max_length=10, default='public', choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')], verbose_name='Publish status')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('body', models.TextField(verbose_name='Body')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(verbose_name='Modified at', auto_now=True)),
                ('publish_at', models.DateTimeField(verbose_name='Published at', null=True, editable=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='Author')),
                ('category', models.ForeignKey(null=True, to='blogs.Category', blank=True, verbose_name='Category')),
            ],
            options={
                'verbose_name_plural': 'Entries',
                'ordering': ('-updated_at', 'title'),
                'permissions': (('view_entry', 'Can view the entry'),),
                'verbose_name': 'Entry',
            },
            bases=(models.Model,),
        ),
    ]
