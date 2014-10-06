# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import kawaz.apps.profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_state', models.CharField(verbose_name='Publish State', choices=[('public', 'Public'), ('protected', 'Internal')], default='public', max_length=10)),
                ('username', models.CharField(verbose_name='Username', max_length=64)),
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
                ('pub_state', models.CharField(verbose_name='Publish status', choices=[('public', 'Public'), ('protected', 'Internal')], default='public', max_length=10)),
                ('birthday', models.DateField(verbose_name='Birth day', null=True, blank=True)),
                ('place', models.CharField(verbose_name='Address', max_length=255, help_text='Your address will not be shown by anonymous user.', blank=True)),
                ('url', models.URLField(verbose_name='URL', max_length=255, blank=True)),
                ('remarks', models.TextField(verbose_name='Remarks')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, editable=False, related_name='profile', verbose_name='User', serialize=False)),
                ('created_at', models.DateTimeField(verbose_name='Created at', auto_now_add=True)),
                ('updated_at', models.DateTimeField(verbose_name='Updated at', auto_now=True)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
                'ordering': ('user__nickname',),
                'permissions': (('view_profile', 'Can view the profile'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(verbose_name='Label', unique=True, max_length=64)),
                ('icon', models.ImageField(verbose_name='Icon', upload_to=kawaz.apps.profiles.models.Service._get_upload_path)),
                ('url_pattern', models.CharField(verbose_name='URL pattern', null=True, max_length=256, blank=True)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(verbose_name='Label', unique=True, max_length=32)),
                ('description', models.CharField(verbose_name='Description', max_length=128)),
                ('order', models.IntegerField(verbose_name='Order', default=0)),
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
            field=models.ManyToManyField(to='profiles.Skill', verbose_name='Skills', null=True, related_name='users', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='profile',
            field=models.ForeignKey(to='profiles.Profile', editable=False, related_name='accounts', verbose_name='Account'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='account',
            name='service',
            field=models.ForeignKey(to='profiles.Service', verbose_name='Service'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('service', 'username')]),
        ),
    ]
