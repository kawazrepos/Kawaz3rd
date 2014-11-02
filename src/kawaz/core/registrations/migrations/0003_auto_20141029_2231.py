# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0002_auto_20141026_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationsupplement',
            name='place',
            field=models.CharField(help_text='居住地を書いてください。札幌市または近郊都市の在住、もしくは出身などで札幌に縁のある必要があります。', verbose_name='場所', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='registrationsupplement',
            name='skill',
            field=models.TextField(help_text='どのようなことができるか、またはゲームに関連したやりたいことを書いてください。', verbose_name='できること', max_length=2048),
            preserve_default=True,
        ),
    ]
