# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import kawaz.core.personas.profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20141014_2146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name_plural': 'アカウント', 'permissions': (('view_account', 'Can view the account'),), 'verbose_name': 'アカウント'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ('user__nickname',), 'verbose_name_plural': 'プロフィール', 'permissions': (('view_profile', 'Can view the profile'),), 'verbose_name': 'プロフィール'},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ('pk',), 'verbose_name_plural': 'サービス', 'verbose_name': 'サービス'},
        ),
        migrations.AlterModelOptions(
            name='skill',
            options={'ordering': ('order', 'pk'), 'verbose_name_plural': 'できること', 'verbose_name': 'できること'},
        ),
        migrations.AlterField(
            model_name='account',
            name='profile',
            field=models.ForeignKey(to='profiles.Profile', editable=False, verbose_name='アカウント', related_name='accounts'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='pub_state',
            field=models.CharField(max_length=10, default='public', choices=[('public', '外部公開'), ('protected', '内部公開')], verbose_name='プロフィールの公開状態'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='service',
            field=models.ForeignKey(to='profiles.Service', verbose_name='サービス'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=64, verbose_name='ユーザ名'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='birthday',
            field=models.DateField(null=True, blank=True, verbose_name='誕生日'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='place',
            field=models.CharField(max_length=255, help_text='住所はKawazメンバーのみ見ることができ、外部ユーザには見えません。', blank=True, verbose_name='住んでるところ'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='pub_state',
            field=models.CharField(max_length=10, default='public', choices=[('public', '外部公開'), ('protected', '内部公開')], verbose_name='公開設定'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(to='profiles.Skill', null=True, related_name='users', blank=True, verbose_name='できること'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='最終更新日'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, editable=False, verbose_name='ユーザ', primary_key=True, related_name='profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='service',
            name='icon',
            field=models.ImageField(upload_to=kawaz.core.personas.profiles.models.Service._get_upload_path, verbose_name='アイコン'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='service',
            name='label',
            field=models.CharField(max_length=64, verbose_name='ラベル', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='service',
            name='url_pattern',
            field=models.CharField(max_length=256, blank=True, verbose_name='ユーザID', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='description',
            field=models.CharField(max_length=128, verbose_name='概要'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='label',
            field=models.CharField(max_length=32, verbose_name='ラベル', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='order',
            field=models.IntegerField(default=0, verbose_name='並び順'),
            preserve_default=True,
        ),
    ]
