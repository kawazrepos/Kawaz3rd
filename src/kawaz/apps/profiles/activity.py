# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/15
#
from django.contrib.contenttypes.models import ContentType
from activities.models import Activity
from kawaz.apps.profiles.models import Account
from kawaz.core.personas.models import Persona

__author__ = 'giginet'
from activities.mediator import ActivityMediator

class ProfileActivityMediator(ActivityMediator):
    use_snapshot = True

    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'updated':
            if activity.previous:
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
                    'url',
                    'birthday',
                )
                for attribute in attributes:
                    if is_updated(attribute):
                        remarks.append(attribute + '_updated')
                if not remarks:
                    # 通知が必要な変更ではないため通知しない
                    return None
                activity.remarks = "\n".join(remarks)
        return activity

    def prepare_context(self, activity, context, typename=None):
        context = super().prepare_context(activity, context, typename)

        if activity.status == 'updated':
            # remarks に保存された変更状態を利便のためフラグ化
            for flag in activity.remarks.split():
                context[flag] = True
        elif activity.status in ('user_add', 'user_removed'):
            # アカウントの追加を通知
            account = Account.objects.get(pk=int(activity.remarks))
            context['account'] = account
        return context


class AccountActivityMediator(ActivityMediator):
    def alter(self, instance, activity, **kwargs):
        if activity.status == 'updated':
            # アップデート時は通知しない
            return None
        if activity:
            # account作成のActivityを親のProfileに所属させる
            profile = instance.profile
            ct = ContentType.objects.get_for_model(type(profile))
            pk = profile.pk
            activity.content_type = ct
            activity.object_id = pk
            if activity.status == "created":
                activity.status = 'account_add'
            elif activity.status == 'deleted':
                activity.status = 'account_remove'
            activity.remarks = instance.pk
            activity.save()
        return activity
