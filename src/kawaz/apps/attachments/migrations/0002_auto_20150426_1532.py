# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP Address', editable=False),
        ),
    ]
