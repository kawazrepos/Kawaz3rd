from django.test import TestCase, override_settings

__author__ = 'giginet'

class ErrorPageTestCase(TestCase):

    @override_settings(DEBUG=False)
    def test_render_404(self):
        """
        本番環境でカスタム404ページが描画できる
        """
        r = self.client.get("/this/page/is/not/found/")
        self.assertEqual(r.status_code, 404)
        self.assertTemplateUsed(r, '404.html')

    # TODO : Test 403/500/favicon

