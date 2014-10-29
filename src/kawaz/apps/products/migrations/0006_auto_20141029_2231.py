# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20141028_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='administrators',
            field=models.ManyToManyField(verbose_name='プロジェクトの管理者', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='display_mode',
            field=models.CharField(help_text='作品のトップページでの表示形態です。「ギミック表示」を利用する場合は「告知用画像」を設定する必要があります。', verbose_name='表示モード', choices=[('featured', 'ギミック表示: トップページのカルーセル + トップページにタイル表示'), ('tiled', 'タイル表示: トップページにタイル表示'), ('normal', '通常表示: 詳細ページにタイル表示（トップページには表示されません）')], default='normal', max_length=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(help_text="作品のURLとして利用されるため半角英数字、半角アンダーバー（'_'）もしくは半角ハイフン（'-'）のみが使用できます。また、URLの変更を防ぐためこの値は一度設定すると変更できません。'XXX'という値を設定すると'http://kawaz.org/products/XXX'のように使用されます", verbose_name='作品ID', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='trailer',
            field=models.URLField(help_text='YouTubeの動画URLを入力すると、作品ページに埋め込むことができます。', verbose_name='トレイラー', blank=True, null=True),
            preserve_default=True,
        ),
    ]
