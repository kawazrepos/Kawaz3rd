# -*- coding: utf-8 -*-
import pickle
from django.db import migrations
from ..registry import registry


def convert_snapshots(apps, schema_editor):
    Activity = apps.get_model('activities', 'Activity')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    for activity in Activity.objects.all():
        ct = ContentType.objects.get(pk=activity.content_type_id)
        natural_key = "{}.{}".format(ct.app_label, ct.model)
        mediator = registry._registry[natural_key]
        snapshot = pickle.loads(activity._snapshot)
        if isinstance(snapshot, dict):
            continue
        serialized_snapshot = mediator.serialize_snapshot(snapshot)
        activity._snapshot = pickle.dumps(serialized_snapshot)
        activity.save()


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '__latest__'),
        ('activities', '0002_test'),
    ]

    operations = [
        migrations.RunPython(convert_snapshots),
    ]
