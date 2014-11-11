# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/15
#
from django_comments import Comment
from activities.mediator import ActivityMediator

__author__ = 'giginet'

class PersonaActivityMediator(ActivityMediator):

    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'updated':
            if activity.previous:
                # 通知が必要な状態の変更を詳細に記録する
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
                    'gender',
                    'avatar',
                    'is_active',
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
            else:
                # previousがないとき、通知しない
                return None
        return activity

    def prepare_context(self, activity, context, typename=None):
        context = super().prepare_context(activity, context, typename)
        if activity.status == 'updated' or activity.status == 'profile_updated':
            # remarks に保存された変更状態を利便のためフラグ化
            # また、プロフィールの更新についてもcontextを発行している
            for flag in activity.remarks.split():
                context[flag] = True
        elif activity.status == 'add_account':
            # アカウントが付いたとき、remarksにaccountのpkが入ってるはずなので
            # 取得してcontextに渡す
            # ついでにserviceも渡している
            try:
                from ..models import Account
                account = Account.objects.get(pk=int(activity.remarks))
                context['account'] = account
                context['service'] = account.service
            except:
                pass
        elif activity.status == 'add_comment':
            # コメントが付いたとき、remarksにcommentのpkが入ってるはずなので
            # 取得してcontextに渡す
            try:
                comment = Comment.objects.get(pk=int(activity.remarks))
                context['comment'] = comment
            except:
                pass
        return context
