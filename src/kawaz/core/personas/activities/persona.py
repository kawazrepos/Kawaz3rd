from django_comments import Comment
from activities.mediator import ActivityMediator
from ..models.persona import Persona


class PersonaActivityMediatorBase(ActivityMediator):
    def serialize_snapshot(self, snapshot):
        serialized_snapshot = super().serialize_snapshot(snapshot)
        if isinstance(snapshot, Persona):
            # スナップショット対象がペルソナの場合対応するプロフィール状態
            # もスナップショットとして保持しておく
            profile = getattr(snapshot, '_profile', None)
            profile = super().serialize_snapshot(profile) if profile else None
            serialized_snapshot['extra_fields'] = {
                '_profile': profile,
            }
        return serialized_snapshot


class PersonaActivityMediator(PersonaActivityMediatorBase):
    """
    Note:
        Personaは3つのMediatorからさまざまなイベントが発行される
        activated: Profileの作成（ユーザーのアクティベート時にプロフィールが
                   作成されるため、プロフィールが生成されたときをアクティベート
                   されたと判定している）
        profile_updated: プロフィールの更新
        comment_added: コメントの追加
        account_added: アカウントの追加

        updatedイベントは初回更新時の前回との差分がないとき、`last_login`カラム
        が更新されるだけでも通知されてしまう問題があり対処が面倒なので、ユーザ
        の更新は一切通知されない仕様にする
    """

    def alter(self, instance, activity, **kwargs):
        if activity.status in ('created', 'updated', 'deleted'):
            # 作成、更新、削除イベントは通知しない
            return None
        return activity

    def prepare_context(self, activity, context, typename=None):
        context = super().prepare_context(activity, context, typename)
        if activity.status in ('updated', 'profile_updated'):
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
