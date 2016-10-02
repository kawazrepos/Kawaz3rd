from django.core.urlresolvers import reverse
from django.test import TestCase
import django_comments
from django_comments.models import Comment
from kawaz.core.comments.forms import KawazCommentForm
from kawaz.core.comments.tests.factories import CommentFactory
from kawaz.core.personas.tests.factories import PersonaFactory


class CommentViewTestCase(TestCase):

    def setUp(self):
        self.user = PersonaFactory()

    def test_post_comment(self):
        """
        コメント投稿用のビューからコメントが投稿できる
        """
        target = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        url = django_comments.get_form_target()
        form = KawazCommentForm(target)
        dict = {field.html_name: field.value() for field in form}
        dict['comment'] = "Hello"
        r = self.client.post(url, {
            'object_pk': dict['object_pk'],
            'content_type': dict['content_type'],
            'security_hash': dict['security_hash'],
            'timestamp': dict['timestamp'],
            'comment': dict['comment'],
        })
        self.assertEqual(r.status_code, 302)

        # コメントが生成されている
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 1)

    def test_not_allowed_empty_comment(self):
        """
        空コメントを投稿できない
        """
        target = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        url = django_comments.get_form_target()
        form = KawazCommentForm(target)
        dict = {field.html_name: field.value() for field in form}
        r = self.client.post(url, {
            'object_pk': dict['object_pk'],
            'content_type': dict['content_type'],
            'security_hash': dict['security_hash'],
            'timestamp': dict['timestamp'],
            'comment': '', # 空文字
        })
        self.assertEqual(r.status_code, 200)

        # コメントが生成できない
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 0)

    def test_can_moderate_via_comments_delete(self):
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
