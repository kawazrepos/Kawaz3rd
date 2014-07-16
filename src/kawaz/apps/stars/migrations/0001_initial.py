# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('object_id', models.PositiveIntegerField(verbose_name='Object ID')),
                ('quote', models.CharField(help_text='This is used for quotation. When the user add a star with text selection, the selected text is passed to this.', blank=True, verbose_name='Quote', max_length=512, default='')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Created at')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', verbose_name='Content Type')),
            ],
            options={
                'permissions': (('view_star', 'Can view the Star'),),
                'ordering': ('created_at',),
                'verbose_name': 'Star',
                'verbose_name_plural': 'Stars',
            },
            bases=(models.Model,),
        ),
    ]
