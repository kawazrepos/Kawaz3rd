# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/15
#
from django_comments import Comment
from activities.mediator import ActivityMediator

__author__ = 'giginet'

class PersonaActivityMediator(ActivityMediator):
    """
    Note:
        Personaは3つのMediatorからさまざまなイベントが発行される
        activated: Profileの作成（ユーザーのアクティベート時にプロフィールが作成されるため、
        プロフィールが生成されたときをアクティベートされたと判定している）
        profile_updated: プロフィールの更新
        comment_added: コメントの追加
        account_added: アカウントの追加

        updatedイベントは初回更新時の前回との差分がないとき、`last_login`カラムが更新されるだけでも通知されてしまう問題があり
        対処が面倒なので、ユーザーの更新は一切通知されない仕様にする
    """

    def alter(self, instance, activity, **kwargs):
        if activity.status in ('created', 'updated', 'deleted'):
            # 作成、更新、削除イベントは通知しない
            return None
        return activity

    def prepare_context(self, activity, context, typename=None):
        context = super().prepare_context(activity, context, typename)
        if activity.status == 'updated' or activity.status == 'profile_updated':
            # remarks に保存された変更状態を利便のためフラグ化
            # また、プロフィールの更新についてもcontextを発行している
            for flag in activity.remarks.split():
                context[flag] = True
            if activity.status == 'profile_updated':
                context['profile'] = activity.snapshot._profile
        elif activity.status == 'account_added':
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
        elif activity.status == 'comment_added':
            # コメントが付いたとき、remarksにcommentのpkが入ってるはずなので
            # 取得してcontextに渡す
            try:
                comment = Comment.objects.get(pk=int(activity.remarks))
                context['comment'] = comment
            except:
                pass
        return context
