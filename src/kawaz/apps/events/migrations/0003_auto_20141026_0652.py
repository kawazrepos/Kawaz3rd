# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20141014_2146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('order',), 'verbose_name_plural': 'ラベル', 'verbose_name': 'ラベル'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('period_start', 'period_end', '-created_at', '-updated_at', 'title', '-pk'), 'verbose_name_plural': 'イベント', 'permissions': (('attend_event', 'Can attend the event'), ('quit_event', 'Can quit the event'), ('view_event', 'Can view the event')), 'verbose_name': 'イベント'},
        ),
        migrations.AlterField(
            model_name='category',
            name='label',
            field=models.CharField(max_length=16, verbose_name='ラベル', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='order',
            field=models.PositiveSmallIntegerField(verbose_name='並び順'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='attendance_deadline',
            field=models.DateTimeField(null=True, default=None, blank=True, verbose_name='参加締切日', help_text='参加締切日を設定できます。この日時を過ぎた場合、参加することはできません'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='events_attend', verbose_name='参加者', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='body',
            field=models.TextField(verbose_name='本文'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.ForeignKey(blank=True, verbose_name='カテゴリ', null=True, to='events.Category'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='number_restriction',
            field=models.PositiveIntegerField(null=True, default=None, blank=True, verbose_name='参加可能人数', help_text='参加人数に上限を設けたい場合に設定してください'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='主催者', null=True, related_name='events_owned'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='period_end',
            field=models.DateTimeField(null=True, blank=True, verbose_name='終了日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='period_start',
            field=models.DateTimeField(null=True, blank=True, verbose_name='開始日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=255, blank=True, verbose_name='場所'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='pub_state',
            field=models.CharField(max_length=10, default='public', choices=[('public', '外部公開'), ('protected', '内部公開'), ('draft', '下書き')], verbose_name='公開設定'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(max_length=255, verbose_name='タイトル'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='event',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='更新日時'),
            preserve_default=True,
        ),
    ]
