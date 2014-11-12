from django.contrib.contenttypes.models import ContentType
from activities.mediator import ActivityMediator

__author__ = 'giginet'

class ProfileActivityMediator(ActivityMediator):
    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'updated':
            # あるユーザーのプロフィールが更新されたとき
            # そのActivityをプロフィールについてではなく、
            # そのプロフィールの持ち主のユーザーに所属させる
            target = instance.user
            ct = ContentType.objects.get_for_model(type(target))
            pk = target.pk
            activity.content_type = ct
            activity.object_id = pk
            activity.status = 'profile_updated'
            # snapshotはPersonaのものになるため
            # Profileの情報を取り出せない
            # そのため、フラグをremarksに設定していない
        return activity


class AccountActivityMediator(ActivityMediator):
    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'created':
            # プロフィールに新しくサービスアカウントが作成されたとき
            # このActivityをユーザーの物にしてしまう
            # また、ステータスも`add_account`に変える
            # remarksには付いたアカウントのPKを入れる
            target = instance.profile.user
            ct = ContentType.objects.get_for_model(type(target))
            pk = target.pk
            activity.content_type = ct
            activity.object_id = pk
            activity.status = 'add_account'
            activity.remarks = str(instance.pk)
            return activity
