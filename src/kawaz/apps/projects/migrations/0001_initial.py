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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('label', models.CharField(verbose_name='Name', unique=True, max_length=32)),
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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('pub_state', models.CharField(default='public', verbose_name='Publish status', choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')], max_length=10)),
                ('status', models.CharField(default='planning', verbose_name='Status', choices=[('planning', 'Planning'), ('active', 'Active'), ('paused', 'Suspended'), ('eternal', 'Eternaled'), ('done', 'Released')], max_length=15)),
                ('title', models.CharField(verbose_name='Title', unique=True, max_length=127)),
                ('slug', models.SlugField(verbose_name='Project slug', unique=True, max_length=63, help_text="It will be used on the url of the project thus it only allow alphabetical or numeric characters, underbar ('_'), and hyphen ('-'). Additionally this value cannot be modified for preventing the URL changes.")),
                ('body', models.TextField(verbose_name='Description')),
                ('icon', thumbnailfield.fields.ThumbnailField(blank=True, verbose_name='Thumbnail', upload_to=kawaz.apps.projects.models.Project._get_upload_path)),
                ('created_at', models.DateTimeField(verbose_name='Created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='Updated at', auto_now=True)),
                ('tracker', models.URLField(default='', blank=True, verbose_name='Tracker URL', help_text='Kawaz RedmineのプロジェクトURLを入力してください')),
                ('repository', models.URLField(default='', blank=True, verbose_name='Repository URL', help_text='Kawaz GitLab, GitHubなどのプロジェクトURLを入力してください')),
                ('administrator', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='Administrator', related_name='projects_owned')),
                ('category', models.ForeignKey(blank=True, to='projects.Category', verbose_name='Category', help_text='Contact us if you cannot find a category you need.', null=True, related_name='projects')),
                ('members', models.ManyToManyField(editable=False, verbose_name='Members', related_name='projects_joined', to=settings.AUTH_USER_MODEL)),
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
