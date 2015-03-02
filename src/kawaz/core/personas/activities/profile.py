from django.contrib.contenttypes.models import ContentType
from activities.mediator import ActivityMediator
from .persona import PersonaActivityMediatorBase


class ProfileActivityMediator(PersonaActivityMediatorBase):
    def alter(self, instance, activity, **kwargs):
        if activity and activity.status in ('created', 'updated'):
            # あるユーザーのプロフィールが更新、作成されたとき
            # そのActivityをプロフィールについてではなく、
            # そのプロフィールの持ち主のユーザーに所属させる
            ct = ContentType.objects.get_for_model(instance.user)
            activity.content_type = ct
            activity.object_id = instance.user.pk
            if activity.status == 'updated':
                activity.status = 'profile_updated'
            elif activity.status == 'created':
                # プロフィールが作成されたとき、activatedステータスを発行する
                activity.status = 'activated'
            # snapshotはPersonaのものになるため
            # Profileの情報を取り出せない
            # そのため、フラグをremarksに設定していない
            return activity
        # 削除イベントでは通知しない
        return None


class AccountActivityMediator(PersonaActivityMediatorBase):
    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'created':
            # プロフィールに新しくサービスアカウントが作成されたとき
            # このActivityをユーザーの物にしてしまう
            # また、ステータスも`account_added`に変える
            # remarksには付いたアカウントのPKを入れる
            target = instance.profile.user
            ct = ContentType.objects.get_for_model(instance.profile.user)
            activity.content_type = ct
            activity.object_id = instance.profile.user.pk
            activity.status = 'account_added'
            activity.remarks = str(instance.pk)
            return activity
