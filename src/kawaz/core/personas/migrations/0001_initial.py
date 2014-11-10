# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.utils.timezone
import thumbnailfield.fields
import kawaz.core.personas.models.persona
import kawaz.core.personas.models.profile
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('username', models.CharField(unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], max_length=30, verbose_name='username', help_text='Required. 30 characters or fewer. Letters, digits and /-/_ only.')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email address', blank=True)),
                ('is_active', models.BooleanField(verbose_name='active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('nickname', models.CharField(max_length=30, verbose_name='Nickname')),
                ('quotes', models.CharField(max_length=127, verbose_name='Mood message', blank=True)),
                ('avatar', thumbnailfield.fields.ThumbnailField(verbose_name='Avatar', upload_to=kawaz.core.personas.models.persona.Persona._get_upload_path, blank=True)),
                ('gender', models.CharField(verbose_name='Gender', max_length=10, default='unknown', choices=[('man', 'Man'), ('woman', 'Woman'), ('unknown', 'Unknown')])),
                ('role', models.CharField(verbose_name='Role', help_text='The role this user belongs to. A user will get permissions of the role thus the user cannot change ones role for security reason.', max_length=10, default='wille', choices=[('adam', 'Adam'), ('seele', 'Seele'), ('nerv', 'Nerv'), ('children', 'Children'), ('wille', 'Wille')])),
            ],
            options={
                'ordering': ('username',),
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
                'permissions': (('activate_persona', 'Can activate/deactivate the persona'), ('assign_role_persona', 'Can assign the role to the persona')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('pub_state', models.CharField(verbose_name='Publish status', max_length=10, default='public', choices=[('public', 'Public'), ('protected', 'Internal')])),
                ('username', models.CharField(max_length=64, verbose_name='Username')),
            ],
            options={
                'verbose_name': 'Account',
                'verbose_name_plural': 'Accounts',
                'permissions': (('view_account', 'Can view the account'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('pub_state', models.CharField(verbose_name='Publish status', max_length=10, default='public', choices=[('public', 'Public'), ('protected', 'Internal')])),
                ('birthday', models.DateField(verbose_name='Birthday', null=True, blank=True)),
                ('place', models.CharField(max_length=255, verbose_name='Address', blank=True)),
                ('url', models.URLField(max_length=255, verbose_name='URL', blank=True)),
                ('remarks', models.TextField(verbose_name='Remarks')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, editable=False, verbose_name='User', related_name='_profile', serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(verbose_name='Updated at', auto_now=True)),
            ],
            options={
                'ordering': ('user__nickname',),
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'permissions': (('view_profile', 'Can view the profile'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('label', models.CharField(unique=True, max_length=64, verbose_name='Label')),
                ('icon', models.ImageField(verbose_name='Icon', upload_to=kawaz.core.personas.models.profile.Service._get_upload_path)),
                ('url_pattern', models.CharField(max_length=256, verbose_name='URL pattern', null=True, blank=True)),
            ],
            options={
                'ordering': ('pk',),
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('label', models.CharField(unique=True, max_length=32, verbose_name='Label')),
                ('description', models.CharField(max_length=128, verbose_name='Description')),
                ('order', models.IntegerField(verbose_name='Order', default=0)),
            ],
            options={
                'ordering': ('order', 'pk'),
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(to='personas.Skill', related_name='users', verbose_name='Skills', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='profile',
            field=models.ForeignKey(to='personas.Profile', editable=False, verbose_name='Account', related_name='accounts'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='service',
            field=models.ForeignKey(to='personas.Service', verbose_name='Service'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('service', 'username')]),
        ),
        migrations.AddField(
            model_name='persona',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', related_query_name='user', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set', verbose_name='groups'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='persona',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', related_query_name='user', blank=True, help_text='Specific permissions for this user.', related_name='user_set', verbose_name='user permissions'),
            preserve_default=True,
        ),
    ]
