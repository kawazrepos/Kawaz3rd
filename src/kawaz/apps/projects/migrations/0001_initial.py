# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kawaz.apps.projects.models
import thumbnailfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=32, verbose_name='Name', unique=True)),
                ('parent', models.ForeignKey(null=True, verbose_name='Parent category', blank=True, to='projects.Category')),
            ],
            options={
                'ordering': ('label',),
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('pub_state', models.CharField(max_length=10, verbose_name='Publish status', choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')], default='public')),
                ('status', models.CharField(max_length=15, verbose_name='Status', choices=[('planning', 'Planning'), ('active', 'Active'), ('eternal', 'Eternaled'), ('done', 'Released')], default='planning')),
                ('title', models.CharField(max_length=127, verbose_name='Title', unique=True)),
                ('slug', models.SlugField(help_text="It will be used on the url of the project thus it only allow alphabetical or numeric characters, underbar ('_'), and hyphen ('-'). Additionally this value cannot be modified for preventing the URL changes.", max_length=63, verbose_name='Project slug', unique=True)),
                ('body', models.TextField(verbose_name='Description')),
                ('icon', thumbnailfield.fields.ThumbnailField(upload_to=kawaz.apps.projects.models.Project._get_upload_path, verbose_name='Thumbnail', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(verbose_name='Updated at', auto_now=True)),
                ('administrator', models.ForeignKey(verbose_name='Administrator', to=settings.AUTH_USER_MODEL, editable=False)),
                ('category', models.ForeignKey(null=True, verbose_name='Category', help_text='Contact us if you cannot find a category you need.', blank=True, to='projects.Category')),
                ('group', models.ForeignKey(verbose_name='Group', to='auth.Group', editable=False, unique=True)),
                ('members', models.ManyToManyField(verbose_name='Members', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('status', '-updated_at', 'title'),
                'verbose_name': 'Project',
                'permissions': (('join_project', 'Can join to the project'), ('quit_project', 'Can quit from the project'), ('view_project', 'Can view the project')),
                'verbose_name_plural': 'Projects',
            },
            bases=(models.Model,),
        ),
    ]
