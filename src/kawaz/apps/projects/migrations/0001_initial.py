# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import thumbnailfield.fields
import kawaz.apps.projects.models
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
                ('label', models.CharField(max_length=32, verbose_name='Category name', unique=True)),
            ],
            options={
                'ordering': ('label',),
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('pub_state', models.CharField(max_length=10, default='public', choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')], verbose_name='Publish status')),
                ('status', models.CharField(max_length=15, default='planning', choices=[('planning', 'Planning'), ('active', 'Active'), ('paused', 'Suspended'), ('eternal', 'Eternaled'), ('done', 'Released')], verbose_name='Status')),
                ('title', models.CharField(max_length=127, verbose_name='Title', unique=True)),
                ('slug', models.SlugField(max_length=63, help_text="It will be used on the url of the project thus it only allow alphabetical or numeric characters, underbar ('_'), and hyphen ('-'). Additionally this value cannot be modified for preventing the URL changes.", verbose_name='Project slug', unique=True)),
                ('body', models.TextField(verbose_name='Description')),
                ('icon', thumbnailfield.fields.ThumbnailField(upload_to=kawaz.apps.projects.models.Project._get_upload_path, blank=True, verbose_name='Thumbnail')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('tracker', models.URLField(blank=True, default='', help_text='Kawaz RedmineのプロジェクトURLを入力してください', verbose_name='Tracker URL')),
                ('repository', models.URLField(blank=True, default='', help_text='Kawaz GitLab, GitHubなどのプロジェクトURLを入力してください', verbose_name='Repository URL')),
                ('administrator', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, related_name='projects_owned', verbose_name='Administrator')),
                ('category', models.ForeignKey(to='projects.Category', help_text='Contact us if you cannot find a category you need.', related_name='projects', null=True, blank=True, verbose_name='Category')),
                ('last_modifier', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, related_name='last_modified_projects', null=True, verbose_name='Last modified by')),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL, editable=False, related_name='projects_joined', verbose_name='Members')),
            ],
            options={
                'permissions': (('join_project', 'Can join to the project'), ('quit_project', 'Can quit from the project'), ('view_project', 'Can view the project')),
                'ordering': ('status', '-updated_at', 'title'),
                'verbose_name_plural': 'Projects',
                'verbose_name': 'Project',
            },
            bases=(models.Model,),
        ),
    ]
