from django.test import TestCase
from activities.models import Activity
from .factories import CommentTestArticleFactory
from .factories import CommentFactory

__author__ = 'giginet'


class CommentActivityMediatorTestCase(TestCase):

    def test_add_comment(self):
        """
        あるオブジェクトにコメントが付いたとき、そのオブジェクトのイベントとして、`add_comment`Activityが付く
        """
        object = CommentTestArticleFactory()

        nactivities = Activity.objects.get_for_object(object).count()

        # コメントをする
        CommentFactory(content_object=object)

        activities = Activity.objects.get_for_object(object)
        self.assertEqual(nactivities + 1, activities.count())

        activity = activities[0]
        self.assertEqual(activity.status, 'add_comment')
        self.assertEqual(activity.snapshot, object)
