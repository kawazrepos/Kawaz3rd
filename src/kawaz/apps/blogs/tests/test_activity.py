from django.template import Context
from activities.registry import registry
from activities.models import Activity
from kawaz.apps.blogs.tests.factories import EntryFactory
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase


class EntryActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = EntryFactory

    def test_create(self):
        self._test_create()

    def test_update(self):
        self._test_partial_update(
            context_names=('title_updated', 'body_updated'),
            title="タイトル変えました",
            body='本文変えました'
        )

    def test_delete(self):
        self._test_delete()

    def test_comment_added(self):
        self._test_comment_added()

    def test_entry_is_published(self):
        draft_entry = EntryFactory(pub_state='draft')

        # draftなエントリーはActivityが作られない
        activities = Activity.objects.get_for_object(draft_entry)
        self.assertEqual(len(activities), 0)

        draft_entry.pub_state = 'public'
        draft_entry.save()

        activities = Activity.objects.get_for_object(draft_entry)
        activity = activities[0]
        self.assertEqual(activity.status, 'updated')
        mediator = registry.get(activity)
        context = Context()
        context = mediator.prepare_context(activity, context)
        self.assertTrue(
            'published' in context,
            'context variable published is not contained'
        )
        mediator = registry.get(activity)
        rendered = mediator.render(activity, {})
        self.assertTrue('公開されました' in rendered)
