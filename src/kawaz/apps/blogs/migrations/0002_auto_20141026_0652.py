# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ('-updated_at', 'title'), 'verbose_name_plural': 'ブログ記事', 'permissions': (('view_entry', 'Can view the entry'),), 'verbose_name': 'ブログ記事'},
        ),
        migrations.AlterField(
            model_name='category',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='作者', related_name='blog_categories'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='label',
            field=models.CharField(max_length=255, verbose_name='カテゴリ名'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='作者', related_name='blog_entries'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='body',
            field=models.TextField(verbose_name='本文'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='category',
            field=models.ForeignKey(to='blogs.Category', blank=True, verbose_name='カテゴリ', null=True, related_name='entries'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='pub_state',
            field=models.CharField(max_length=10, default='public', choices=[('public', '外部公開'), ('protected', '内部公開'), ('draft', '下書き')], verbose_name='公開設定'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='publish_at',
            field=models.DateTimeField(null=True, verbose_name='公開日', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='title',
            field=models.CharField(max_length=255, verbose_name='タイトル'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='entry',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新日時'),
            preserve_default=True,
        ),
    ]
