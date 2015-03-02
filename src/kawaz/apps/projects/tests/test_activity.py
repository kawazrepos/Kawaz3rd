from .factories import ProjectFactory
from kawaz.core.activities.tests.testcases import BaseActivityMediatorTestCase


class ProjectActivityMediatorTestCase(BaseActivityMediatorTestCase):
    factory_class = ProjectFactory

    def test_create(self):
        self._test_create()

    def test_update(self):
        self._test_partial_update(body='本文変えました')

    def test_delete(self):
        self._test_delete()

    def test_comment_added(self):
        self._test_comment_added()
