# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import kawaz.apps.profiles.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('pub_state', models.CharField(choices=[('public', 'Public'), ('protected', 'Internal')], verbose_name='Publish State', max_length=10, default='public')),
                ('username', models.CharField(verbose_name='Username', max_length=64)),
            ],
            options={
                'permissions': (('view_account', 'Can view the account'),),
                'verbose_name_plural': 'Accounts',
                'verbose_name': 'Account',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('pub_state', models.CharField(choices=[('public', 'Public'), ('protected', 'Internal')], verbose_name='Publish status', max_length=10, default='public')),
                ('birthday', models.DateField(blank=True, verbose_name='Birth day', null=True)),
                ('place', models.CharField(blank=True, verbose_name='Address', max_length=255, help_text='Your address will not be shown by anonymous user.')),
                ('url', models.URLField(blank=True, verbose_name='URL', max_length=255)),
                ('remarks', models.TextField(verbose_name='Remarks')),
                ('created_at', models.DateTimeField(verbose_name='Created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='Updated at', auto_now=True)),
                ('user', models.OneToOneField(primary_key=True, editable=False, to=settings.AUTH_USER_MODEL, serialize=False, verbose_name='User')),
            ],
            options={
                'permissions': (('view_profile', 'Can view the profile'),),
                'verbose_name_plural': 'Profiles',
                'verbose_name': 'Profile',
                'ordering': ('user__nickname',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='account',
            name='profile',
            field=models.ForeignKey(verbose_name='Account', to='profiles.Profile', editable=False),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(unique=True, verbose_name='Label', max_length=64)),
                ('icon', models.ImageField(upload_to=kawaz.apps.profiles.models.Service._get_upload_path, verbose_name='Icon')),
                ('url_pattern', models.CharField(blank=True, null=True, verbose_name='URL pattern', max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Services',
                'verbose_name': 'Service',
                'ordering': ('pk',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='account',
            name='service',
            field=models.ForeignKey(verbose_name='Service', to='profiles.Service'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('service', 'username')]),
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(unique=True, verbose_name='Label', max_length=32)),
                ('description', models.CharField(verbose_name='Description', max_length=128)),
                ('order', models.IntegerField(verbose_name='Order', default=0)),
            ],
            options={
                'verbose_name_plural': 'Skills',
                'verbose_name': 'Skill',
                'ordering': ('order', 'pk'),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(blank=True, verbose_name='Skills', null=True, to='profiles.Skill'),
            preserve_default=True,
        ),
    ]
