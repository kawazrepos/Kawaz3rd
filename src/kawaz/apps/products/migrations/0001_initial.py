# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import thumbnailfield.fields
import kawaz.apps.products.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('label', models.CharField(unique=True, max_length=32, verbose_name='Label')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('label', models.CharField(max_length=32, verbose_name='Label')),
                ('version', models.CharField(default='', max_length=32, verbose_name='Version')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('file_content', models.FileField(upload_to=kawaz.apps.products.models.PackageRelease._get_upload_path, verbose_name='File')),
                ('downloads', models.PositiveIntegerField(default=0, help_text='The number of downloads', verbose_name='Downloads', editable=False)),
            ],
            options={
                'ordering': ('platform__pk', 'product__pk'),
                'abstract': False,
                'verbose_name_plural': 'Package releases',
                'verbose_name': 'Package release',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('label', models.CharField(unique=True, max_length=32, verbose_name='Label')),
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
        migrations.AddField(
            model_name='packagerelease',
            name='platform',
            field=models.ForeignKey(verbose_name='Platform', to='products.Platform'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(unique=True, max_length=128, verbose_name='Title')),
                ('slug', models.SlugField(unique=True, help_text="It will be used on the url of the product thus it only allow alphabetical or numeric characters, underbar ('_'), and hyphen ('-'). Additionally this value cannot be modified for preventing the URL changes.", verbose_name='Product slug')),
                ('thumbnail', thumbnailfield.fields.ThumbnailField(upload_to=kawaz.apps.products.models.Product._get_thumbnail_upload_path, help_text='This would be used as a product thumbnail image. The aspect ratio of the image should be 16:9.', verbose_name='Thumbnail')),
                ('description', models.TextField(max_length=4096, verbose_name='Description')),
                ('advertisement_image', thumbnailfield.fields.ThumbnailField(null=True, verbose_name='Advertisement Image', blank=True, upload_to=kawaz.apps.products.models.Product._get_advertisement_image_upload_path, help_text='This would be used in the top page. The aspect ratio of the image should be 16:9')),
                ('trailer', models.URLField(null=True, help_text='Enter URL of your trailer movie on the YouTube. The movie would be embeded to the product page.', verbose_name='Trailer', blank=True)),
                ('publish_at', models.DateField(verbose_name='Publish at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('display_mode', models.CharField(default='normal', choices=[('featured', 'Featured'), ('tiled', 'Tiled'), ('normal', 'Normal')], help_text='How the product displayed on the site top. To use `featured`, it require `advertisement_image`.', max_length=10, verbose_name='Display mode')),
                ('administrators', models.ManyToManyField(verbose_name='Administrators', editable=False, to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(verbose_name='Categories', to='products.Category')),
                ('platforms', models.ManyToManyField(verbose_name='Platforms', to='products.Platform')),
                ('project', models.ForeignKey(null=True, verbose_name='Project', blank=True, to='projects.Project')),
            ],
            options={
                'ordering': ('display_mode', '-publish_at'),
                'verbose_name_plural': 'Products',
                'verbose_name': 'Product',
                'permissions': (('join_product', 'Can join to the product'), ('quit_product', 'Can quit from the product')),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='packagerelease',
            name='product',
            field=models.ForeignKey(editable=False, verbose_name='Product', to='products.Product'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('image', thumbnailfield.fields.ThumbnailField(upload_to=kawaz.apps.products.models.Screenshot._get_upload_path, verbose_name='Image')),
                ('product', models.ForeignKey(editable=False, verbose_name='Product', to='products.Product')),
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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('label', models.CharField(max_length=32, verbose_name='Label')),
                ('version', models.CharField(default='', max_length=32, verbose_name='Version')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('url', models.URLField(verbose_name='URL')),
                ('pageview', models.PositiveIntegerField(default=0, help_text='The number of page views', verbose_name='Page view', editable=False)),
                ('platform', models.ForeignKey(verbose_name='Platform', to='products.Platform')),
                ('product', models.ForeignKey(editable=False, verbose_name='Product', to='products.Product')),
            ],
            options={
                'ordering': ('platform__pk', 'product__pk'),
                'abstract': False,
                'verbose_name_plural': 'URL releases',
                'verbose_name': 'URL release',
            },
            bases=(models.Model,),
        ),
    ]
