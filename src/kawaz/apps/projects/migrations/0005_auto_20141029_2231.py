# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20141028_2352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(help_text="プロジェクトのURLとして利用されるため半角英数字、半角アンダーバー（'_'）もしくは半角ハイフン（'-'）のみが使用できます。また、URLの変更を防ぐためこの値は一度設定すると変更できません。'XXX'という値を設定すると'http://kawaz.org/project/XXX'のように使用されます", verbose_name='プロジェクトID', unique=True, max_length=63),
            preserve_default=True,
        ),
    ]
