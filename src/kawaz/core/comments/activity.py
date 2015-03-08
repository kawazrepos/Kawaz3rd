from django.contrib.contenttypes.models import ContentType
from kawaz.core.personas.models import Persona
from activities.models import Activity
from activities.mediator import ActivityMediator
from activities.registry import registry


class CommentActivityMediator(ActivityMediator):

    def translate_snapshot(self, snapshot):
        # 可能な限り対象モデルに合わせたスナップショットを作成する
        try:
            mediator = registry.get(snapshot)
        except KeyError:
            mediator = super()
        return mediator.translate_snapshot(snapshot)

    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'created':
            target = instance.content_object
            # あるモデルにコメントが付いたことを通知させるため
            # コメントが作成されたタイミングで、そのアクティビティを
            # コメントが追加されたオブジェクトの物に変えてしまう
            # また、ステータスも`comment_added`に変える
            ct = ContentType.objects.get_for_model(type(target))
            pk = target.pk
            activity.content_type = ct
            activity.object_id = pk
            activity.status = 'comment_added'
            activity.remarks = str(instance.pk)
            return activity
