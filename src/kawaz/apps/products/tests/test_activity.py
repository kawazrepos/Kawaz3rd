from django.template import Context
from activities.registry import registry
from activities.models import Activity
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase
from .factories import (ProductFactory,
                        PackageReleaseFactory,
                        URLReleaseFactory,
                        ScreenshotFactory)


class ProductActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = ProductFactory

    def test_create(self):
        self._test_create()

    def test_update(self):
        self._test_partial_update(
            (
                'description_updated',
                'title_updated',
                'trailer_updated',
                'thumbnail_updated'
            ),
            description='本文変えました',
            title="タイトル変えました",
            trailer='http://example.com',
            thumbnail='hoge.png')

    def test_delete(self):
        self._test_delete()

    def test_comment_added(self):
        self._test_comment_added()

    def test_package_release_added(self):
        """
        PackageReleaseを追加したときに、release_addedが発行される
        """
        nactivities = Activity.objects.get_for_object(self.object).count()

        # PackageReleaseを作る
        release = PackageReleaseFactory(product=self.object)

        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(nactivities + 1, activities.count())

        activity = activities[0]
        self.assertEqual(activity.status, 'release_added')
        self.assertEqual(activity.snapshot, self.object)
        # remarksにリリースのapp_label,model,pkが入る
        remarks = 'products,packagerelease,{}'.format(release.pk)
        self.assertEqual(activity.remarks, remarks)

        self._test_render(activity)
        mediator = registry.get(activity)
        context = mediator.prepare_context(activity, Context())
        self.assertIn('release', context, "context doesn't contain 'release'")

    def test_url_release_added(self):
        """
        URLReleaseを追加したときに、release_addedが発行される
        """
        nactivities = Activity.objects.get_for_object(self.object).count()

        # URLReleaseを作る
        release = URLReleaseFactory(product=self.object)

        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(nactivities + 1, activities.count())

        activity = activities[0]
        self.assertEqual(activity.status, 'release_added')
        self.assertEqual(activity.snapshot, self.object)
        # remarksにリリースのapp_label,model,pkが入る
        remarks = 'products,urlrelease,{}'.format(release.pk)
        self.assertEqual(activity.remarks, remarks)

        self._test_render(activity)
        mediator = registry.get(activity)
        context = mediator.prepare_context(activity, Context())
        self.assertIn('release', context, "context doesn't contain 'release'")

    def test_package_release_updated(self):
        """
        Package Releaseがアップデートされても更新通知されない
        """
        release = PackageReleaseFactory(product=self.object)
        nactivities = Activity.objects.get_for_object(self.object).count()

        release.downloads += 1
        release.save()
        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(nactivities, activities.count())

    def test_url_release_updated(self):
        """
        URL Releaseがアップデートされても更新通知されない
        """
        release = URLReleaseFactory(product=self.object)
        nactivities = Activity.objects.get_for_object(self.object).count()

        release.pageview += 1
        release.save()
        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(nactivities, activities.count())

    def test_screenshot_added(self):
        """
        Screenshotを追加したときに、screenshot_addedが発行される
        """
        nactivities = Activity.objects.get_for_object(self.object).count()

        # Screenshotを作る
        ss = ScreenshotFactory(product=self.object)

        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(nactivities + 1, activities.count())

        activity = activities[0]
        self.assertEqual(activity.status, 'screenshot_added')
        self.assertEqual(activity.snapshot, self.object)
        # remarksにスクリーンショットのpkが入る
        remarks = str(ss.pk)
        self.assertEqual(activity.remarks, remarks)

        self._test_render(activity)
        mediator = registry.get(activity)
        context = mediator.prepare_context(activity, Context())
        self.assertIn('screenshot', context,
                      "context doesn't contain 'screenshot'")
