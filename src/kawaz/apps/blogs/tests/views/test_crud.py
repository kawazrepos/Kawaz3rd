import urllib
from django.core.urlresolvers import reverse
from django.utils.timezone import datetime, get_default_timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import AnonymousUser
from ..factories import EntryFactory
from ..factories import CategoryFactory
from ...models import Entry
from kawaz.core.personas.tests.factories import PersonaFactory

class EntryDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()

    def test_anonymous_user_can_view_public_entry(self):
        '''Tests anonymous user can view public entry'''
        entry = EntryFactory()
        r = self.client.get(entry.get_absolute_url())
        self.assertTemplateUsed(r, 'blogs/entry_detail.html')
        self.assertEqual(r.context_data['object'], entry)

    def test_authorized_user_can_view_public_entry(self):
        '''Tests authorized user can view public entry'''
        entry = EntryFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(entry.get_absolute_url())
        self.assertTemplateUsed(r, 'blogs/entry_detail.html')
        self.assertEqual(r.context_data['object'], entry)

    def test_anonymous_user_can_not_view_protected_entry(self):
        '''Tests anonymous user can not view protected entry'''
        entry = EntryFactory(pub_state='protected')
        r = self.client.get(entry.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, entry.get_absolute_url()))

    def test_authorized_user_can_view_protected_entry(self):
        '''Tests authorized user can view public entry'''
        entry = EntryFactory(pub_state='protected')
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(entry.get_absolute_url())
        self.assertTemplateUsed(r, 'blogs/entry_detail.html')
        self.assertEqual(r.context_data['object'], entry)

    def test_anonymous_user_can_not_view_draft_entry(self):
        '''Tests anonymous user can not view draft entry'''
        entry = EntryFactory(pub_state='draft')
        r = self.client.get(entry.get_absolute_url())
        self.assertRedirects(r, '{0}?next={1}'.format(settings.LOGIN_URL, entry.get_absolute_url()))

    def test_others_can_not_view_draft_entry(self):
        '''
        Tests others can not view draft entry
        User will redirect to '/entries/{entry.pk}/update/'
        '''
        entry = EntryFactory(pub_state='draft')
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(entry.get_absolute_url())
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/{0}/{1}/update/'.format(entry.author.username, entry.pk))

    def test_organizer_can_view_draft_entry(self):
        '''Tests organizer can view draft entry on update view'''
        entry = EntryFactory(pub_state='draft', author=self.user)
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get(entry.get_absolute_url())
        self.assertTemplateUsed(r, 'blogs/entry_form.html')
        self.assertEqual(r.context_data['object'], entry)

class EntryCreateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()

    def test_anonymous_user_can_not_create_view(self):
        '''Tests anonymous user can not view EntryCreateView'''
        r = self.client.get('/blogs/{}/create/'.format(self.user.username))
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/{}/create/'.format(self.user.username))

    def test_authorized_user_can_view_entry_create_view(self):
        '''Tests authorized user can view EntryCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/{}/create/'.format(self.user.username))
        self.assertTemplateUsed(r, 'blogs/entry_form.html')
        self.assertFalse('object' in r.context_data)

    def test_anonymous_user_can_not_create_via_create_view(self):
        '''Tests anonymous user can not create entry via EntryCreateView'''
        r = self.client.post('/blogs/{}/create/'.format(self.user.username), {
            'pub_state' : 'public',
            'title' : '日記です',
            'body' : '天気が良かったです',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/{}/create/'.format(self.user.username))

    def test_authorized_user_can_create_via_create_view(self):
        '''Tests authorized user can create entry via EntryCreateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/blogs/{}/create/'.format(self.user.username), {
            'pub_state' : 'public',
            'title' : '日記です',
            'body' : '天気が良かったです',
        })
        today = datetime.today()
        entry = Entry.objects.last()
        self.assertRedirects(r, '/blogs/{0}/{1}/{2}/{3}/{4}/'.format(self.user.username, today.year, today.month, today.day, entry.pk))
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(entry.title, '日記です')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_user_cannot_modify_author_id(self):
        '''
        Tests authorized user cannot modify author id.
        In entry creation form, `author` is exist as hidden field.
        So user can modify `author` to invalid values.
        This test checks that `author` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/blogs/{0}/create/'.format(self.user.username), {
            'pub_state' : 'public',
            'title' : '日記です',
            'body' : '天気が良かったです',
            'author' : other.pk # crackers attempt to masquerade
        })
        today = datetime.today()
        entry = Entry.objects.last()
        self.assertRedirects(r, '/blogs/{0}/{1}/{2}/{3}/{4}/'.format(self.user.username, today.year, today.month, today.day, entry.pk))
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(entry.author, self.user)
        self.assertNotEqual(entry.author, other)
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_user_can_create_entry_with_category(self):
        """
        カテゴリを指定してブログ記事を新しく投稿できる
        """
        category = CategoryFactory(author=self.user)
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/blogs/{0}/create/'.format(self.user.username), {
            'pub_state': 'public',
            'title': '日記です',
            'body': '天気が良かったです',
            'category': category.pk
        })
        today = datetime.today()
        entry = Entry.objects.last()
        self.assertRedirects(r, '/blogs/{0}/{1}/{2}/{3}/{4}/'.format(self.user.username, today.year, today.month, today.day, entry.pk))
        self.assertEqual(Entry.objects.count(), 1)
        self.assertEqual(entry.author, self.user)
        self.assertEqual(entry.category, category)
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_user_can_create_entry_with_others_category(self):
        """
        他人のカテゴリを指定してブログ記事を新しく投稿しようとすると
        ValidationErrorを送出する
        """
        category = CategoryFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/blogs/{0}/create/'.format(self.user.username), {
                              'pub_state': 'public',
                              'title': '日記です',
                              'body': '天気が良かったです',
                              'category': category.pk
        })
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Entry.objects.count(), 0)


class EntryUpdateViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(username='author_kawaztan')
        self.user.set_password('password')
        self.other = PersonaFactory(username='black_kawaztan')
        self.user.save()
        self.other.save()
        self.entry = EntryFactory(title='かわずたんだよ☆', author=self.user)

    def test_anonymous_user_can_not_view_entry_update_view(self):
        '''Tests anonymous user can not view EntryUpdateView'''
        r = self.client.get('/blogs/author_kawaztan/{}/update/'.format(self.entry.pk))
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/author_kawaztan/{}/update/'.format(self.entry.pk))

    def test_authorized_user_can_view_entry_update_view(self):
        '''
        Tests authorized user can view EntryUpdateView
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/author_kawaztan/{}/update/'.format(self.entry.pk))
        self.assertTemplateUsed(r, 'blogs/entry_form.html')
        self.assertTrue('object' in r.context_data)
        self.assertEqual(r.context_data['object'], self.entry)

    def test_anonymous_user_can_not_update_via_update_view(self):
        '''
        Tests anonymous user can not update entry via EntryUpdateView
        It will redirect to LOGIN_URL
        '''
        r = self.client.post('/blogs/author_kawaztan/{}/update/'.format(self.entry.pk), {
            'pub_state' : 'public',
            'title' : 'クラッカーだよー',
            'body' : 'うえーい',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/author_kawaztan/{}/update/'.format(self.entry.pk))
        self.assertEqual(self.entry.title, 'かわずたんだよ☆')

    def test_other_user_cannot_update_via_update_view(self):
        '''
        Tests other user cannot update entry via EntryUpdateView
        It will redirect to LOGIN_URL
        '''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/blogs/author_kawaztan/{}/update/'.format(self.entry.pk), {
            'pub_state' : 'public',
            'title' : 'いたずら日記です',
            'body' : '黒かわずたんだよーん',
        })
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/author_kawaztan/{}/update/'.format(self.entry.pk))
        self.assertEqual(self.entry.title, 'かわずたんだよ☆')

    def test_author_can_update_via_update_view(self):
        '''Tests author user can update entry via EntryUpdateView'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/blogs/author_kawaztan/{}/update/'.format(self.entry.pk), {
            'pub_state' : 'public',
            'title' : 'やっぱり書き換えます！',
            'body' : 'うえーい',
        })
        tz = get_default_timezone()
        published_at = self.entry.published_at.astimezone(tz)
        self.assertRedirects(r, '/blogs/author_kawaztan/{0}/{1}/{2}/{3}/'.format(published_at.year, published_at.month, published_at.day, self.entry.pk))
        self.assertEqual(Entry.objects.count(), 1)
        entry = Entry.objects.last()
        self.assertEqual(entry.title, 'やっぱり書き換えます！')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")

    def test_user_cannot_modify_author_id(self):
        '''
        Tests authorized user cannot modify author id.
        In entry update form, `author` is exist as hidden field.
        So user can modify `author` to invalid values.
        This test checks that `author` will be set by `request.user`
        '''
        other = PersonaFactory()
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/blogs/author_kawaztan/{}/update/'.format(self.entry.pk), {
            'pub_state' : 'public',
            'title' : 'ID書き換えます！',
            'body' : 'うえーい',
            'author' : other.pk # crackers attempt to masquerade
        })
        tz = get_default_timezone()
        published_at = self.entry.published_at.astimezone(tz)
        self.assertRedirects(r, '/blogs/author_kawaztan/{0}/{1}/{2}/{3}/'.format(published_at.year, published_at.month, published_at.day, self.entry.pk))
        self.assertEqual(Entry.objects.count(), 1)
        entry = Entry.objects.last()
        self.assertEqual(entry.author, self.user)
        self.assertNotEqual(entry.author, other)
        self.assertEqual(entry.title, 'ID書き換えます！')
        self.assertTrue('messages' in r.cookies, "No messages are appeared")


class EntryListViewTestCase(TestCase):
    def setUp(self):
        self.entries = (
            EntryFactory(),
            EntryFactory(pub_state='protected'),
            EntryFactory(pub_state='draft'),
        )
        self.user = PersonaFactory()
        self.user.set_password('password')
        self.user.save()
        self.wille = PersonaFactory(role='wille')
        self.wille.set_password('password')
        self.wille.save()

    def test_context_has_paginator(self):
        """
        EntryListViewのcontextにpaginatorが含まれている
        """
        r = self.client.get('/blogs/')
        self.assertTrue('page_obj' in r.context)
        self.assertTrue('paginator' in r.context)

    def test_paginate_by(self):
        """
        ProjectListViewでは1ページに5個までしかブログが含まれない
        また、ページネーションができていて、次のページには残りのオブジェクトが含まれている
        """
        for i in range(7):
            EntryFactory()
        # setUpで作ったpublic1個と、今作った7個で8こあるはず
        r = self.client.get('/blogs/')
        object_list = r.context['object_list']
        self.assertEqual(len(object_list), 5)

        r = self.client.get('/blogs/?page=2')
        object_list = r.context['object_list']
        self.assertEqual(len(object_list), 3)

    def test_anonymous_can_view_only_public_entries(self):
        '''
        Tests anonymous user can view public Entry only.
        The protected entries are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/blogs/')
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[0])

    def test_wille_can_view_only_public_entries(self):
        '''
        Tests wille user can view public Entry only.
        The protected entries are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/blogs/')
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[0])

    def test_authenticated_can_view_all_publish_entries(self):
        '''
        Tests authenticated user can view all published entries.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/')
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entries')
        self.assertIn(self.entries[1], list, 'protected')
        self.assertIn(self.entries[0], list, 'public')


class EntryAuthorListViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory()
        self.wille = PersonaFactory(role='wille')
        self.entries = (
            EntryFactory(),
            EntryFactory(author=self.user),
            EntryFactory(pub_state='protected'),
            EntryFactory(pub_state='protected', author=self.user),
            EntryFactory(pub_state='draft'),
        )

    def test_context_has_paginator(self):
        """
        EntryAuthorListViewのcontextにpaginatorが含まれている
        """
        r = self.client.get('/blogs/{}/'.format(self.user.username))
        self.assertTrue('page_obj' in r.context)
        self.assertTrue('paginator' in r.context)
        self.assertEqual(r.context_data['author'], self.user)

    def test_paginate_by(self):
        """
        ProjectListViewでは1ページに5個までしかブログが含まれない
        また、ページネーションができていて、次のページには残りのオブジェクトが含まれている
        """
        for i in range(7):
            EntryFactory(author=self.user)
        # setUpで作ったpublic1個と、今作った7個で8こあるはず
        r = self.client.get('/blogs/{}/'.format(self.user.username))
        self.assertTrue('page_obj' in r.context)
        object_list = r.context['object_list']
        self.assertEqual(len(object_list), 5)
        self.assertEqual(r.context_data['author'], self.user)

        r = self.client.get('/blogs/{}/?page=2'.format(self.user.username))
        object_list = r.context['object_list']
        self.assertEqual(len(object_list), 3)
        self.assertEqual(r.context_data['author'], self.user)

    def test_anonymous_can_view_only_public_entries_of_the_author(self):
        '''
        Tests anonymous user can view public Entry written by specific author only.
        The protected entries are not displayed.
        '''
        user = AnonymousUser()
        r = self.client.get('/blogs/{}/'.format(self.user.username))
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[1])
        self.assertEqual(r.context_data['author'], self.user)

    def test_wille_can_view_only_public_entries_of_the_author(self):
        '''
        Tests wille user can view public Entry written by specific author only.
        The protected entries are not displayed.
        '''
        self.assertTrue(self.client.login(username=self.wille, password='password'))
        r = self.client.get('/blogs/{}/'.format(self.user.username))
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 1, 'object_list has one entry')
        self.assertEqual(list[0], self.entries[1])
        self.assertEqual(r.context_data['author'], self.user)

    def test_authenticated_can_view_all_publish_entries_of_the_author(self):
        '''
        Tests authenticated user can view all published entries written by specific author.
        '''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.get('/blogs/{}/'.format(self.user.username))
        self.assertTemplateUsed('blogs/entry_list.html')
        self.assertTrue('object_list' in r.context_data)
        list = r.context_data['object_list']
        self.assertEqual(list.count(), 2, 'object_list has two entries')
        self.assertIn(self.entries[3], list, 'protected')
        self.assertIn(self.entries[1], list, 'public')
        self.assertEqual(r.context_data['author'], self.user)


class EntryPreviewViewTestCase(TestCase):
    def test_preview(self):
        """
        ユーザーがEntryのPreviewを見れる
        """
        import json
        r = self.client.post('/blogs/preview/', json.dumps({}), content_type='application/json')
        self.assertTemplateUsed(r, 'blogs/components/entry_detail.html')

class EntryCategoryListView(TestCase):

    def test_category_url(self):
        """
        blogs_entry_category_listから
        /blogs/<author>/category/<category_pk>/が引ける
        """
        author = PersonaFactory()
        category = CategoryFactory()

        self.assertEqual(reverse('blogs_entry_category_list',
                                 kwargs={'author' :author.username, 'pk': category.pk}),
                         '/blogs/{}/category/{}/'.format(author.username, category.pk))

    def test_category_list(self):
        """
        カテゴリ一に属してる記事一覧が見れる
        """
        user0 = PersonaFactory()
        user1 = PersonaFactory()
        category0 = CategoryFactory(author=user0, label="ゲームレビュー")
        category1 = CategoryFactory(author=user1, label="ゲームレビュー")
        entry0 = EntryFactory(category=category0, author=user0)
        entry1 = EntryFactory(category=category0, author=user0)
        entry2 = EntryFactory(category=category1, author=user1)
        entry3 = EntryFactory(category=category1, pub_state='draft', author=user1)

        url = '/blogs/{}/category/{}/'.format(user0.username, category0.pk)
        r = self.client.get(url)
        self.assertEqual(len(r.context['object_list']), 2)
        self.assertTrue(entry0 in r.context['object_list'])
        self.assertTrue(entry1 in r.context['object_list'])

        url = '/blogs/{}/category/{}/'.format(user1.username, category1.pk)
        r = self.client.get(url)
        self.assertTrue(len(r.context['object_list']), 1)
        self.assertTrue(entry2 in r.context['object_list'])

        self.assertTrue('author' in r.context)


class EntryDeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = PersonaFactory(username='author_kawaztan')
        self.user.set_password('password')
        self.other = PersonaFactory(username='black_kawaztan')
        self.user.save()
        self.other.save()
        self.entry = EntryFactory(title='かわずたんだよ☆', author=self.user)

    def test_anonymous_user_can_not_delete_via_delete_view(self):
        '''非ログインユーザーは記事の削除ができない'''
        r = self.client.post('/blogs/author_kawaztan/{}/delete/'.format(self.entry.pk))
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/author_kawaztan/{}/delete/'.format(self.entry.pk))
        self.assertEqual(self.entry.title, 'かわずたんだよ☆')

    def test_other_user_cannot_delete_via_delete_view(self):
        '''作者以外のユーザーは記事の削除ができない'''
        self.assertTrue(self.client.login(username=self.other, password='password'))
        r = self.client.post('/blogs/author_kawaztan/{}/delete/'.format(self.entry.pk))
        self.assertRedirects(r, settings.LOGIN_URL + '?next=/blogs/author_kawaztan/{}/delete/'.format(self.entry.pk))
        self.assertEqual(self.entry.title, 'かわずたんだよ☆')

    def test_author_can_delete_via_delete_view(self):
        '''作者は記事を削除できる'''
        self.assertTrue(self.client.login(username=self.user, password='password'))
        r = self.client.post('/blogs/author_kawaztan/{}/delete/'.format(self.entry.pk))
        self.assertRedirects(r, '/blogs/')
        self.assertEqual(Entry.objects.count(), 0)
