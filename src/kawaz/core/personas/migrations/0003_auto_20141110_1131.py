# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0002_test'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='persona',
            options={'verbose_name': 'Persona', 'verbose_name_plural': 'Personas', 'permissions': (('activate_persona', 'Can activate/deactivate the persona'), ('assign_role_persona', 'Can assign the role to the persona')), 'ordering': ('username',)},
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(verbose_name='Username', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='persona',
            name='gender',
            field=models.CharField(choices=[('man', 'Man'), ('woman', 'Woman'), ('unknown', 'Unknown')], verbose_name='Gender', max_length=10, default='unknown'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='persona',
            name='username',
            field=models.CharField(verbose_name='username', unique=True, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and /-/_ only.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(verbose_name='User', related_name='_profile', to=settings.AUTH_USER_MODEL, editable=False, primary_key=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='skill',
            name='order',
            field=models.IntegerField(verbose_name='Order', default=0),
            preserve_default=True,
        ),
    ]
