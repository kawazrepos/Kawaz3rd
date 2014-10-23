# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/23
#
from django.contrib.contenttypes.models import ContentType
from kawaz.core.personas.models import Persona
from activities.models import Activity
from activities.mediator import ActivityMediator

__author__ = 'giginet'

class CommentActivityMediator(ActivityMediator):

    def alter(self, instance, activity, **kwargs):
        if activity and activity.status == 'created':
            target = instance.content_object
            # あるモデルにコメントが付いたことを通知させるため
            # コメントが作成されたタイミングで、そのアクティビティを
            # コメントが追加されたオブジェクトの物に変えてしまう
            # また、ステータスも`add_comment`に変える
            ct = ContentType.objects.get_for_model(type(target))
            pk = target.pk
            activity.content_type = ct
            activity.object_id = pk
            activity.status = 'add_comment'
            return activity
