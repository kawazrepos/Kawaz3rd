# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationsupplement',
            name='place',
            field=models.CharField(max_length=64, help_text='札幌市または近郊都市の在住、もしくは出身などで札幌に縁のある必要があります。', verbose_name='場所'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='registrationsupplement',
            name='remarks',
            field=models.TextField(null=True, blank=True, verbose_name='一言メッセージ'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='registrationsupplement',
            name='skill',
            field=models.TextField(max_length=2048, help_text='どのようなことができるか、またはどのようなゲームが作りたいか書いてください。', verbose_name='できること'),
            preserve_default=True,
        ),
    ]
