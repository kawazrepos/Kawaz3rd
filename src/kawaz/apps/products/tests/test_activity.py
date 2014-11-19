# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/18
#
from django.contrib.contenttypes.models import ContentType
from django.template import Context
from activities.registry import registry
from activities.models import Activity
from kawaz.apps.products.tests.factories import ProductFactory, PackageReleaseFactory, URLReleaseFactory, \
    ScreenshotFactory
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase

__author__ = 'giginet'


class ProductActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = ProductFactory

    def test_create(self):
        self._test_create()

    def test_update(self):
        self._test_partial_update(description='本文変えました')

    def test_delete(self):
        self._test_delete()

    def test_comment_add(self):
        self._test_comment_add()

    def test_add_package_release(self):
        """
        PackageReleaseを追加したときに、release_addが発行される
        """
        nactivities = Activity.objects.get_for_object(self.object).count()

        # PackageReleaseを作る
        release = PackageReleaseFactory(product=self.object)

        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(nactivities + 1, activities.count())

        activity = activities[0]
        self.assertEqual(activity.status, 'release_add')
        self.assertEqual(activity.snapshot, self.object)
        # remarksにリリースのapp_label,model,pkが入る
        ct = ContentType.objects.get_for_model(type(release))
        ct = ContentType.objects.get_for_model(type(release))
        remarks = 'products,packagerelease,{}'.format(release.pk)
        self.assertEqual(activity.remarks, remarks)

        self._test_render(activity)
        mediator = registry.get(activity)
        context = mediator.prepare_context(activity, Context())
        self.assertTrue('release' in context, """context doesn't contain 'release'""")

    def test_add_url_release(self):
        """
        URLReleaseを追加したときに、release_addが発行される
        """
        nactivities = Activity.objects.get_for_object(self.object).count()

        # URLReleaseを作る
        release = URLReleaseFactory(product=self.object)

        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(nactivities + 1, activities.count())

        activity = activities[0]
        self.assertEqual(activity.status, 'release_add')
        self.assertEqual(activity.snapshot, self.object)
        # remarksにリリースのapp_label,model,pkが入る
        ct = ContentType.objects.get_for_model(type(release))
        remarks = 'products,urlrelease,{}'.format(release.pk)
        self.assertEqual(activity.remarks, remarks)

        self._test_render(activity)
        mediator = registry.get(activity)
        context = mediator.prepare_context(activity, Context())
        self.assertTrue('release' in context, """context doesn't contain 'release'""")

    def test_screenshot_add(self):
        """
        Screenshotを追加したときに、screenshot_addが発行される
        """
        nactivities = Activity.objects.get_for_object(self.object).count()

        # Screenshotを作る
        ss = ScreenshotFactory(product=self.object)

        activities = Activity.objects.get_for_object(self.object)
        self.assertEqual(nactivities + 1, activities.count())

        activity = activities[0]
        self.assertEqual(activity.status, 'screenshot_add')
        self.assertEqual(activity.snapshot, self.object)
        # remarksにスクリーンショットのpkが入る
        remarks = str(ss.pk)
        self.assertEqual(activity.remarks, remarks)

        self._test_render(activity)
        mediator = registry.get(activity)
        context = mediator.prepare_context(activity, Context())
        self.assertTrue('screenshot' in context, """context doesn't contain 'screenshot'""")
