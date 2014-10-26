# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0002_announcement_last_modifier'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='announcement',
            options={'ordering': ('-created_at',), 'verbose_name_plural': 'お知らせ', 'permissions': (('view_announcement', 'Can view the announcement'),), 'verbose_name': 'お知らせ'},
        ),
        migrations.AlterField(
            model_name='announcement',
            name='body',
            field=models.TextField(verbose_name='本文'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='last_modifier',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='最終更新者', null=True, related_name='last_modified_announcements'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='pub_state',
            field=models.CharField(max_length=10, default='public', choices=[('public', '外部公開'), ('protected', '内部公開'), ('draft', '下書き')], verbose_name='公開設定'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='title',
            field=models.CharField(max_length=128, verbose_name='タイトル'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='announcement',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新日時'),
            preserve_default=True,
        ),
    ]
