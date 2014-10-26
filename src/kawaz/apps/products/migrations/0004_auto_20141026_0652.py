# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import kawaz.apps.products.models
import thumbnailfield.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_last_modifier'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('order', 'pk'), 'verbose_name_plural': 'カテゴリ', 'verbose_name': 'カテゴリ'},
        ),
        migrations.AlterModelOptions(
            name='packagerelease',
            options={'ordering': ('platform__pk', 'product__pk'), 'verbose_name_plural': 'パッケージ', 'verbose_name': 'パッケージ'},
        ),
        migrations.AlterModelOptions(
            name='platform',
            options={'ordering': ('order', 'pk'), 'verbose_name_plural': 'プラットフォーム', 'verbose_name': 'プラットフォーム'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('display_mode', '-publish_at'), 'verbose_name_plural': '作品', 'permissions': (('join_product', 'Can join to the product'), ('quit_product', 'Can quit from the product')), 'verbose_name': '作品'},
        ),
        migrations.AlterModelOptions(
            name='screenshot',
            options={'ordering': ('pk',), 'verbose_name_plural': 'スクリーンショット', 'verbose_name': 'スクリーンショット'},
        ),
        migrations.AlterModelOptions(
            name='urlrelease',
            options={'ordering': ('platform__pk', 'product__pk'), 'verbose_name_plural': 'URL', 'verbose_name': 'URL'},
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(max_length=128, verbose_name='概要'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='label',
            field=models.CharField(max_length=32, verbose_name='ラベル', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='category',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, help_text='この値が小さい順に並びます', verbose_name='並び順'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='packagerelease',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='packagerelease',
            name='downloads',
            field=models.PositiveIntegerField(help_text='ダウンロード数', default=0, verbose_name='ダウンロード', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='packagerelease',
            name='label',
            field=models.CharField(max_length=32, verbose_name='ラベル'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='packagerelease',
            name='platform',
            field=models.ForeignKey(to='products.Platform', verbose_name='プラットフォーム'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='packagerelease',
            name='product',
            field=models.ForeignKey(to='products.Product', editable=False, verbose_name='作品', related_name='packagereleases'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='packagerelease',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='最終更新日'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='packagerelease',
            name='version',
            field=models.CharField(max_length=32, default='', verbose_name='バージョン'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='platform',
            name='icon',
            field=models.ImageField(upload_to=kawaz.apps.products.models.Platform._get_upload_path, verbose_name='アイコン'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='platform',
            name='label',
            field=models.CharField(max_length=32, verbose_name='ラベル', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='platform',
            name='order',
            field=models.PositiveSmallIntegerField(default=0, help_text='この値が小さい順に並びます', verbose_name='並び順'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='administrators',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='プロジェクトの管理者', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='advertisement_image',
            field=thumbnailfield.fields.ThumbnailField(blank=True, verbose_name='告知用画像', null=True, help_text='この作品をKawazのトップページに表示したい場合、そのための画像を設定できます。アスペクト比16:9で設定すると綺麗に表示されます。', upload_to=kawaz.apps.products.models.Product._get_advertisement_image_upload_path),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(to='products.Category', verbose_name='カテゴリ'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=4096, verbose_name='概要'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='display_mode',
            field=models.CharField(max_length=10, default='normal', choices=[('featured', 'トップページのカルーセル + トップページにタイル表示'), ('tiled', 'トップページにタイル表示'), ('normal', 'トップページには表示されず、詳細ページでのみタイル表示')], verbose_name='表示モード', help_text='この作品をトップページへカルーセル + タイル表示する場合、告知用画像を設定する必要があります。'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='last_modifier',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, verbose_name='最終更新者', null=True, related_name='last_modified_products'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='platforms',
            field=models.ManyToManyField(to='products.Platform', verbose_name='プラットフォーム'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='project',
            field=models.ForeignKey(blank=True, verbose_name='プロジェクト', null=True, to='projects.Project'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='publish_at',
            field=models.DateField(verbose_name='公開日'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(help_text='作品のURLとなる文字列を設定してください。半角英数字、半角アンダーバー、半角ハイフンのみ使用できます。一度設定すると変更することはできません。このように設定されます。http://kawaz.org/products/xxxxxxxxxxxx', verbose_name='作品ID', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='thumbnail',
            field=thumbnailfield.fields.ThumbnailField(help_text='作品のサムネイルとなる画像を設定できます。アスペクト比16:9で設定すると綺麗に表示されます。', upload_to=kawaz.apps.products.models.Product._get_thumbnail_upload_path, verbose_name='サムネイル'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=128, verbose_name='タイトル', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='trailer',
            field=models.URLField(help_text='Youtubeの動画URLを入力すると、作品ページに埋め込むことができます。', blank=True, verbose_name='トレイラー', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='最終更新日'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='screenshot',
            name='product',
            field=models.ForeignKey(to='products.Product', editable=False, verbose_name='作品', related_name='screenshots'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlrelease',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='作成日時'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlrelease',
            name='label',
            field=models.CharField(max_length=32, verbose_name='ラベル'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlrelease',
            name='pageview',
            field=models.PositiveIntegerField(help_text='閲覧数', default=0, verbose_name='閲覧数', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlrelease',
            name='platform',
            field=models.ForeignKey(to='products.Platform', verbose_name='プラットフォーム'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlrelease',
            name='product',
            field=models.ForeignKey(to='products.Product', editable=False, verbose_name='作品', related_name='urlreleases'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlrelease',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='最終更新日'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='urlrelease',
            name='version',
            field=models.CharField(max_length=32, default='', verbose_name='バージョン'),
            preserve_default=True,
        ),
    ]
