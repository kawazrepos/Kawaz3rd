# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kawaz.apps.projects.models
import thumbnailfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_project_last_modifier'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('label',), 'verbose_name_plural': 'カテゴリ', 'verbose_name': 'カテゴリ'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('status', '-updated_at', 'title'), 'verbose_name_plural': 'プロジェクト', 'permissions': (('join_project', 'Can join to the project'), ('quit_project', 'Can quit from the project'), ('view_project', 'Can view the project')), 'verbose_name': 'プロジェクト'},
        ),
        migrations.AlterField(
            model_name='category',
            name='label',
            field=models.CharField(max_length=32, verbose_name='プロジェクト名', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='administrator',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='管理者', related_name='projects_owned'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='body',
            field=models.TextField(verbose_name='概要'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='category',
            field=models.ForeignKey(to='projects.Category', blank=True, verbose_name='カテゴリ', null=True, help_text='どのカテゴリにも当てはまらない場合はお問い合わせください', related_name='projects'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='icon',
            field=thumbnailfield.fields.ThumbnailField(upload_to=kawaz.apps.projects.models.Project._get_upload_path, blank=True, verbose_name='サムネイル'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='last_modifier',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='最終更新者', null=True, related_name='last_modified_projects'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='projects_joined', verbose_name='所属メンバー', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='pub_state',
            field=models.CharField(max_length=10, default='public', choices=[('public', '外部公開'), ('protected', '内部公開'), ('draft', '下書き')], verbose_name='公開設定'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='repository',
            field=models.URLField(default='', blank=True, verbose_name='リポジトリのURL', help_text='Kawaz GitLab, GitHubなどのプロジェクトURLを入力してください'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(max_length=63, help_text='プロジェクトのURLとなる文字列を設定してください。半角英数字、半角アンダーバー、半角ハイフンのみ使用できます。一度設定すると変更することはできません。このように設定されます。http://kawaz.org/products/xxxxxxxxxxxx', verbose_name='プロジェクトID', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(max_length=15, default='planning', choices=[('planning', '企画中'), ('active', '活動中'), ('paused', '一時停止中'), ('eternal', 'エターナった'), ('done', '完成')], verbose_name='状態'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=127, verbose_name='タイトル', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='tracker',
            field=models.URLField(default='', blank=True, verbose_name='トラッカーのURL', help_text='Kawaz RedmineのプロジェクトURLを入力してください'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='最終更新日'),
            preserve_default=True,
        ),
    ]
