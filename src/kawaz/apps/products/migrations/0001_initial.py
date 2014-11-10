# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import thumbnailfield.fields
import kawaz.apps.products.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('label', models.CharField(max_length=32, verbose_name='Label', unique=True)),
                ('description', models.CharField(max_length=128, verbose_name='Description')),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='この値が小さい順に並びます', verbose_name='Order')),
            ],
            options={
                'ordering': ('order', 'pk'),
                'verbose_name_plural': 'Categories',
                'verbose_name': 'Category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PackageRelease',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('label', models.CharField(max_length=32, verbose_name='Label')),
                ('version', models.CharField(max_length=32, default='', verbose_name='Version')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('file_content', models.FileField(upload_to=kawaz.apps.products.models.PackageRelease._get_upload_path, verbose_name='File')),
                ('downloads', models.PositiveIntegerField(editable=False, default=0, help_text='The number of downloads', verbose_name='Downloads')),
            ],
            options={
                'ordering': ('platform__pk', 'product__pk'),
                'verbose_name_plural': 'Package releases',
                'abstract': False,
                'verbose_name': 'Package release',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('label', models.CharField(max_length=32, verbose_name='Label', unique=True)),
                ('icon', models.ImageField(upload_to=kawaz.apps.products.models.Platform._get_upload_path, verbose_name='Icon')),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='この値が小さい順に並びます', verbose_name='Order')),
            ],
            options={
                'ordering': ('order', 'pk'),
                'verbose_name_plural': 'Platforms',
                'verbose_name': 'Platform',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=128, verbose_name='Title', unique=True)),
                ('slug', models.SlugField(help_text="It will be used on the url of the product thus it only allow alphabetical or numeric characters, underbar ('_'), and hyphen ('-'). Additionally this value cannot be modified for preventing the URL changes.", verbose_name='Product slug', unique=True)),
                ('thumbnail', thumbnailfield.fields.ThumbnailField(upload_to=kawaz.apps.products.models.Product._get_thumbnail_upload_path, help_text='This would be used as a product thumbnail image. The aspect ratio of the image should be 16:9.We recommend the image size to be 800 * 450.', verbose_name='Thumbnail')),
                ('description', models.TextField(max_length=4096, verbose_name='Description')),
                ('advertisement_image', thumbnailfield.fields.ThumbnailField(upload_to=kawaz.apps.products.models.Product._get_advertisement_image_upload_path, help_text='This would be used in the top page. The aspect ratio of the image should be 16:9We recommend the image size to be 800 * 450', null=True, blank=True, verbose_name='Advertisement Image')),
                ('trailer', models.URLField(blank=True, help_text='Enter URL of your trailer movie on the YouTube. The movie would be embeded to the product page.', null=True, verbose_name='Trailer')),
                ('publish_at', models.DateField(verbose_name='Published at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('display_mode', models.CharField(max_length=10, default='normal', help_text="How the product displayed on the top page. To use 'Featured', an 'Advertisement image' is required.", choices=[('featured', 'Fetured: Displayed in the curled cell and the tiled cell on the top page'), ('tiled', 'Tiled: Displayed in the tiled cell on the top page'), ('normal', 'Normal: Displayed only in tiled cell on the detailed page')], verbose_name='Display mode')),
                ('administrators', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Administrators')),
                ('categories', models.ManyToManyField(to='products.Category', verbose_name='Categories')),
                ('last_modifier', models.ForeignKey(to=settings.AUTH_USER_MODEL, editable=False, related_name='last_modified_products', null=True, verbose_name='Last modified by')),
                ('platforms', models.ManyToManyField(to='products.Platform', verbose_name='Platforms')),
                ('project', models.OneToOneField(to='projects.Project', related_name='product', null=True, blank=True, verbose_name='Project')),
            ],
            options={
                'permissions': (('join_product', 'Can join to the product'), ('quit_product', 'Can quit from the product')),
                'ordering': ('display_mode', '-publish_at'),
                'verbose_name_plural': 'Products',
                'verbose_name': 'Product',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('image', thumbnailfield.fields.ThumbnailField(upload_to=kawaz.apps.products.models.Screenshot._get_upload_path, verbose_name='Image')),
                ('product', models.ForeignKey(to='products.Product', editable=False, related_name='screenshots', verbose_name='Product')),
            ],
            options={
                'ordering': ('pk',),
                'verbose_name_plural': 'Screen shots',
                'verbose_name': 'Screen shot',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='URLRelease',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('label', models.CharField(max_length=32, verbose_name='Label')),
                ('version', models.CharField(max_length=32, default='', verbose_name='Version')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('url', models.URLField(verbose_name='URL')),
                ('pageview', models.PositiveIntegerField(editable=False, default=0, help_text='The number of page views', verbose_name='Page view')),
                ('platform', models.ForeignKey(to='products.Platform', verbose_name='Platform')),
                ('product', models.ForeignKey(to='products.Product', editable=False, related_name='urlreleases', verbose_name='Product')),
            ],
            options={
                'ordering': ('platform__pk', 'product__pk'),
                'verbose_name_plural': 'URL releases',
                'abstract': False,
                'verbose_name': 'URL release',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='packagerelease',
            name='platform',
            field=models.ForeignKey(to='products.Platform', verbose_name='Platform'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='packagerelease',
            name='product',
            field=models.ForeignKey(to='products.Product', editable=False, related_name='packagereleases', verbose_name='Product'),
            preserve_default=True,
        ),
    ]
