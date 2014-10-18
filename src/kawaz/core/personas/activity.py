# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/15
#
from django.contrib.contenttypes.models import ContentType
from kawaz.core.personas.models import Persona
from activities.models import Activity
from activities.mediator import ActivityMediator

__author__ = 'giginet'

class PersonaActivityMediator(ActivityMediator):
    use_snapshot = True

    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'updated':
            # 通知が必要な状態の変更を詳細に記録する
            if activity.previous is None:
                activity.status = 'created'
            else:
                previous = activity.previous.snapshot
                is_created = lambda x: (
                    not getattr(previous, x) and
                    getattr(instance, x)
                )
                is_updated = lambda x: (
                    getattr(previous, x) and
                    getattr(instance, x) and
                    getattr(previous, x) != getattr(instance, x)
                )
                is_deleted = lambda x: (
                    getattr(previous, x) and
                    not getattr(instance, x)
                )
                remarks = []
                attributes = (
                    'nickname',
                )
                for attribute in attributes:
                    if is_created(attribute):
                        remarks.append(attribute + '_created')
                    elif is_updated(attribute):
                        remarks.append(attribute + '_updated')
                    elif is_deleted(attribute):
                        remarks.append(attribute + '_deleted')
                if not remarks:
                    # 通知が必要な変更ではないため通知しない
                    return None
                activity.remarks = "\n".join(remarks)
