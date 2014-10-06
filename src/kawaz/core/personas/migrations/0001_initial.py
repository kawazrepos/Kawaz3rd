# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models, migrations
import django.utils.timezone
import django.core.validators
import kawaz.core.personas.models
import thumbnailfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], max_length=30, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, blank=True, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, blank=True, verbose_name='last name')),
                ('email', models.EmailField(max_length=75, blank=True, verbose_name='email address')),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(max_length=30, verbose_name='Nickname')),
                ('quotes', models.CharField(max_length=127, blank=True, verbose_name='Mood message')),
                ('avatar', thumbnailfield.fields.ThumbnailField(blank=True, verbose_name='Avatar', upload_to=kawaz.core.personas.models.Persona._get_upload_path)),
                ('gender', models.CharField(choices=[('man', 'Man'), ('woman', 'Woman'), ('unknown', 'Unknown')], default='unknown', max_length=10, verbose_name='Gender')),
                ('role', models.CharField(help_text='The role this user belongs to. A user will get permissions of the role thus the user cannot change ones role for security reason.', choices=[('adam', 'Adam'), ('seele', 'Seele'), ('nerv', 'Nerv'), ('children', 'Children'), ('wille', 'Wille')], default='wille', max_length=10, verbose_name='Role')),
                ('groups', models.ManyToManyField(to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, related_query_name='user', verbose_name='groups', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', help_text='Specific permissions for this user.', blank=True, related_query_name='user', verbose_name='user permissions', related_name='user_set')),
            ],
            options={
                'verbose_name_plural': 'Personas',
                'verbose_name': 'Persona',
                'ordering': ('username',),
                'permissions': (('view_persona', 'Can view the persona'), ('activate_persona', 'Can activate/deactivate the persona'), ('assign_role_persona', 'Can assign the role to the persona')),
            },
            bases=(models.Model,),
        ),
    ]

    if getattr(settings, 'TESTING'):
        # settings.TESTING is assigned in
        # kawaz.core.tests.runner.KawazDiscoverRunner
        operations.extend([
            migrations.CreateModel(
                name='PersonaTestArticle',
                fields=[
                    ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                    ('pub_state', models.CharField(default='public', max_length=10, choices=[('public', 'Public'), ('protected', 'Internal'), ('draft', 'Draft')], verbose_name='Publish status')),
                    ('title', models.CharField(max_length=255, verbose_name='Title')),
                    ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ],
                options={
                },
                bases=(models.Model,),
            ),
        ])
