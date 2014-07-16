# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import thumbnailfield.fields
import kawaz.core.personas.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.')),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=75)),
                ('is_active', models.BooleanField(default=True, verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(verbose_name='Nickname', max_length=30)),
                ('quotes', models.CharField(blank=True, verbose_name='Mood message', max_length=127)),
                ('avatar', thumbnailfield.fields.ThumbnailField(blank=True, verbose_name='Avatar', upload_to=kawaz.core.personas.models.Persona._get_upload_path)),
                ('gender', models.CharField(default='unknown', choices=[('man', 'Man'), ('woman', 'Woman'), ('unknown', 'Unknown')], verbose_name='Gender', max_length=10)),
                ('role', models.CharField(default='wille', choices=[('adam', 'Adam'), ('seele', 'Seele'), ('nerv', 'Nerv'), ('children', 'Children'), ('wille', 'Wille')], verbose_name='Role', max_length=10, help_text='The role this user belongs to. A user will get permissions of the role thus the user cannot change ones role for security reason.')),
                ('groups', models.ManyToManyField(blank=True, to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('username',),
                'permissions': (('view_persona', 'Can view the persona'), ('activate_persona', 'Can activate/deactivate the persona'), ('assign_role_persona', 'Can assign the role to the persona')),
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
            },
            bases=(models.Model,),
        ),
    ]
