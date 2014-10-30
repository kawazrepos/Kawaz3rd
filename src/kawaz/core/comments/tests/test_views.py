from django.core.urlresolvers import reverse
from django.test import TestCase
from kawaz.core.comments.tests.factories import CommentFactory
from kawaz.core.personas.tests.factories import PersonaFactory

__author__ = 'giginet'

class CommentViewTestCase(TestCase):

    def test_can_delete_via_comment_delete(self):
        """
        comments-deleteから自分のコメントを非表示にできる

        django_commentsの実装から、can_moderateのパーミッションチェックがされていることは保証されているので
        ここでは権限チェックをしていない
        """
        user = PersonaFactory()
        comment = CommentFactory(user=user)
        self.assertTrue(self.client.login(username=user.username, password='password'))

        url = reverse('comments-delete', args=[comment.pk])
        r = self.client.post(url)
        self.assertRedirects(r, '{}?c={}'.format(reverse('comments-delete-done'), comment.pk))

    def test_can_render_delete_done(self):
        """
        comments-delete-doneのテンプレートが表示できる
        """
        url = reverse('comments-delete-done')
        r = self.client.get(url)
        self.assertTemplateUsed(r, 'comments/deleted.html')
