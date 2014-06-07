#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/8
#

from django.test import TestCase

class KawazRoughPageTestCase(TestCase):

    def _test_template(self, name):
        r = self.client.get("/{}/".format(name))
        self.assertTemplateUsed(r, "roughpages/{}.html".format(name))

    def test_access_to_about(self):
        """
        /about/にアクセスして、roughpages/about.htmlが表示できるかどうか
        """
        self._test_template("about")

    def test_access_to_published(self):
        """
        /published/にアクセスして、roughpages/published.htmlが表示できるかどうか
        """
        self._test_template("published")

    def test_access_to_rules(self):
        """
        /rules/にアクセスして、roughpages/rules.htmlが表示できるかどうか
        """
        self._test_template("rules")


