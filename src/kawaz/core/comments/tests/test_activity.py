from unittest.mock import MagicMock
from django.template import Context
from django.test import TestCase
from activities.mediator import ActivityMediator
from activities.models import Activity
from activities.registry import registry
from .factories import CommentTestArticleFactory
from .factories import CommentFactory
from kawaz.core.comments.tests.models import CommentTestArticle

__author__ = 'giginet'


class CommentActivityMediatorTestCase(TestCase):
    def setUp(self):
        registry.register(CommentTestArticle, ActivityMediator())

    def test_add_comment(self):
        """
        あるオブジェクトにコメントが付いたとき、そのオブジェクトのイベントとして、`add_comment`Activityが付く
        """
        object = CommentTestArticleFactory()

        nactivities = Activity.objects.get_for_object(object).count()

        # コメントをする
        comment = CommentFactory(content_object=object)

        activities = Activity.objects.get_for_object(object)
        self.assertEqual(nactivities + 1, activities.count())

        activity = activities[0]
        self.assertEqual(activity.status, 'add_comment')
        self.assertEqual(activity.snapshot, object)
        # remarksにコメントのpkが入る
        self.assertEqual(activity.remarks, str(comment.pk))

    def test_render_add_comment(self):
        """
         render_activityでadd_commentが正しく表示できる
        """
        object = CommentTestArticleFactory()

        nactivities = Activity.objects.get_for_object(object).count()

        # コメントをする
        CommentFactory(content_object=object)

        activities = Activity.objects.get_for_object(object)
        self.assertEqual(nactivities + 1, activities.count())

        activity = activities[0]
        mediator = registry.get(activity)

        self.assertTrue(mediator.render(activity, Context()))
