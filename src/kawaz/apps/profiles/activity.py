# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/15
#
__author__ = 'giginet'
from activities.mediator import ActivityMediator

class ProfileActivityMediator(ActivityMediator):
    use_snapshot = True

    def alter(self, instance, activity, **kwargs):
        # 状態がdraftの場合は通知しない
        if activity and activity.status == 'updated':
            # 通知が必要な状態の変更を詳細に記録する
            previous = activity.previous.snapshot
            is_updated = lambda x: (
                getattr(previous, x) and
                getattr(instance, x) and
                getattr(previous, x) != getattr(instance, x)
            )
            remarks = []
            attributes = (
                'remarks',
                'place',
            )
            for attribute in attributes:
                if is_updated(attribute):
                    remarks.append(attribute + '_updated')
            if not remarks:
                # 通知が必要な変更ではないため通知しない
                return None
            activity.remarks = "\n".join(remarks)
        return activity
