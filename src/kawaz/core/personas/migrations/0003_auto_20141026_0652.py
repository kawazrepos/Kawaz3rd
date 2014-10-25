# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import thumbnailfield.fields
import kawaz.core.personas.models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0002_auto_20141014_2146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='persona',
            options={'ordering': ('username',), 'verbose_name_plural': 'ユーザー', 'permissions': (('view_persona', 'Can view the persona'), ('activate_persona', 'Can activate/deactivate the persona'), ('assign_role_persona', 'Can assign the role to the persona')), 'verbose_name': 'ユーザー'},
        ),
        migrations.AlterField(
            model_name='persona',
            name='avatar',
            field=thumbnailfield.fields.ThumbnailField(upload_to=kawaz.core.personas.models.Persona._get_upload_path, blank=True, verbose_name='ユーザアイコン'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='persona',
            name='gender',
            field=models.CharField(max_length=10, default='unknown', choices=[('man', '男性'), ('woman', '女性'), ('unknown', 'ひみつ')], verbose_name='性別'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='persona',
            name='nickname',
            field=models.CharField(max_length=30, verbose_name='ニックネーム'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='persona',
            name='quotes',
            field=models.CharField(max_length=127, blank=True, verbose_name='一言メッセージ'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='persona',
            name='role',
            field=models.CharField(max_length=10, default='wille', choices=[('adam', 'アダム'), ('seele', 'ゼーレ'), ('nerv', 'ネルフ'), ('children', 'チルドレン'), ('wille', 'ヴィレ')], verbose_name='役職', help_text='ユーザーが所属している役割です。この役割に応じて、ユーザーに権限が与えられます。セキュリティ上の理由から、ユーザーは自分の役割を変更できません。'),
            preserve_default=True,
        ),
    ]
