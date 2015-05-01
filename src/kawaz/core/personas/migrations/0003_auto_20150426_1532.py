# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0002_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address', blank=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='groups',
            field=models.ManyToManyField(help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups', related_query_name='user', related_name='user_set', to='auth.Group', blank=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
        migrations.AlterField(
            model_name='persona',
            name='username',
            field=models.CharField(max_length=30, help_text='Required. 30 characters or fewer. Letters, digits and /-/_ only.', verbose_name='username', error_messages={'unique': 'A user with that username already exists.'}, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(verbose_name='Skills', related_name='users', to='personas.Skill', blank=True),
        ),
    ]
