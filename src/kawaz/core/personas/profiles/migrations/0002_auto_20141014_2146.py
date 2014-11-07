# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(verbose_name='ユーザー名', max_length=64),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, serialize=False, verbose_name='ユーザー', editable=False, primary_key=True, related_name='profile'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='order',
            field=models.IntegerField(verbose_name='並び変え', default=0),
        ),
    ]
