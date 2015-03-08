# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('status', models.CharField(max_length=30)),
                ('remarks', models.TextField(default='')),
                ('object_id', models.PositiveIntegerField(verbose_name='Object ID')),
                ('_snapshot', models.BinaryField(default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'Activity',
                'ordering': ('-created_at',),
                'verbose_name_plural': 'Activities',
            },
            bases=(models.Model,),
        ),
    ]
