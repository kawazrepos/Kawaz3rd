# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import kawaz.core.personas.models.persona
import thumbnailfield.fields
from django.conf import settings
import django.utils.timezone
import kawaz.core.personas.models.profile


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(verbose_name='first name', max_length=30, blank=True)),
                ('last_name', models.CharField(verbose_name='last name', max_length=30, blank=True)),
                ('email', models.EmailField(verbose_name='email address', max_length=75, blank=True)),
                ('is_active', models.BooleanField(help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('nickname', models.CharField(verbose_name='Nickname', max_length=30)),
                ('quotes', models.CharField(verbose_name='Mood message', max_length=127, blank=True)),
                ('avatar', thumbnailfield.fields.ThumbnailField(verbose_name='Avatar', blank=True, upload_to=kawaz.core.personas.models.persona.Persona._get_upload_path)),
                ('gender', models.CharField(default='unknown', max_length=10, choices=[('man', 'Man'), ('woman', 'Woman'), ('unknown', '不明')], verbose_name='Gender')),
                ('role', models.CharField(help_text='The role this user belongs to. A user will get permissions of the role thus the user cannot change ones role for security reason.', default='wille', max_length=10, choices=[('adam', 'Adam'), ('seele', 'Seele'), ('nerv', 'Nerv'), ('children', 'Children'), ('wille', 'Wille')], verbose_name='Role')),
            ],
            options={
                'verbose_name': 'Persona',
                'permissions': (('view_persona', 'Can view the persona'), ('activate_persona', 'Can activate/deactivate the persona'), ('assign_role_persona', 'Can assign the role to the persona')),
                'ordering': ('username',),
                'verbose_name_plural': 'Personas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('pub_state', models.CharField(default='public', max_length=10, choices=[('public', 'Public'), ('protected', 'Internal')], verbose_name='Publish status')),
                ('username', models.CharField(verbose_name='ユーザー名', max_length=64)),
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
                ('pub_state', models.CharField(default='public', max_length=10, choices=[('public', 'Public'), ('protected', 'Internal')], verbose_name='Publish status')),
                ('birthday', models.DateField(verbose_name='Birthday', blank=True, null=True)),
                ('place', models.CharField(verbose_name='Address', max_length=255, blank=True)),
                ('url', models.URLField(verbose_name='URL', max_length=255, blank=True)),
                ('remarks', models.TextField(verbose_name='Remarks')),
                ('user', models.OneToOneField(primary_key=True, editable=False, serialize=False, related_name='_profile', verbose_name='ユーザー', to=settings.AUTH_USER_MODEL)),
                ('created_at', models.DateTimeField(verbose_name='Created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='Updated at', auto_now=True)),
            ],
            options={
                'verbose_name': 'Profile',
                'permissions': (('view_profile', 'Can view the profile'),),
                'ordering': ('user__nickname',),
                'verbose_name_plural': 'Profiles',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='Label', max_length=64, unique=True)),
                ('icon', models.ImageField(verbose_name='Icon', upload_to=kawaz.core.personas.models.profile.Service._get_upload_path)),
                ('url_pattern', models.CharField(verbose_name='URL pattern', max_length=256, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'ordering': ('pk',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('label', models.CharField(verbose_name='Label', max_length=32, unique=True)),
                ('description', models.CharField(verbose_name='Description', max_length=128)),
                ('order', models.IntegerField(default=0, verbose_name='並び変え')),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
                'ordering': ('order', 'pk'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(verbose_name='Skills', blank=True, null=True, to='personas.Skill', related_name='users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='profile',
            field=models.ForeignKey(editable=False, verbose_name='Account', related_name='accounts', to='personas.Profile'),
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
            field=models.ManyToManyField(to='auth.Group', related_name='user_set', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups', blank=True, related_query_name='user'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='persona',
            name='user_permissions',
            field=models.ManyToManyField(to='auth.Permission', related_name='user_set', help_text='Specific permissions for this user.', verbose_name='user permissions', blank=True, related_query_name='user'),
            preserve_default=True,
        ),
    ]
