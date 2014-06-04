import datetime
from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError
from unittest.mock import MagicMock
from kawaz.core.tests.datetime import patch_datetime_now
from kawaz.core.personas.tests.utils import create_role_users
from .utils import static_now
from .utils import event_factory_with_relative


@patch_datetime_now(static_now)     # 2000/09/04
class EventsTemplateTagTestCase(TestCase):
    def setUp(self):
        # イベントリストの作成
        arguments_list = (
            (-3, 0),                                # 2000/9/1-4    Almost
            (-2, -1),                               # 2000/9/2-3    Finish
            (4, 5),                                 # 2000/9/8-9
            (5, 6, {'pub_state': 'draft'}),         # 2000/9/9-10
            (0, 3, {'pub_state': 'protected'}),     # 2000/9/4-7
            (5, 6, {'number_restriction': 1}),      # number restricted
            (5, 6,),                                # deadline
        )
        self.event_list = [event_factory_with_relative(*args)
                           for args in arguments_list]
        # 過去のイベントが作れない制約を回避するために現在時間をモックで変更
        standard_time = static_now()
        attendance_deadline = standard_time - datetime.timedelta(hours=24)
        static_now_past = lambda: static_now() - datetime.timedelta(hours=48)
        with patch_datetime_now(static_now_past):
            self.event_list[-1].attendance_deadline = attendance_deadline
            self.event_list[-1].save()
        # draft 記事の作成者を取得
        self.organizer = self.event_list[3].organizer
        self.users = create_role_users({'organizer': self.organizer})

    def _render_template(self, username, lookup=''):
        t = Template(
            "{{% load events_tags %}}"
            "{{% get_events {} as events %}}".format(
                "'{}'".format(lookup) if lookup else ''
            )
        )
        r = MagicMock()
        r.user = self.users[username]
        c = Context(dict(request=r))
        r = t.render(c)
        # get_blog_events は何も描画しない
        self.assertEqual(r.strip(), "")
        return c['events']

    def test_get_events_published(self):
        """get_events published はユーザーに対して公開された記事を返す"""
        patterns = (
            ('adam', 6),
            ('seele', 6),
            ('nerv', 6),
            ('children', 6),
            ('wille', 5),
            ('anonymous', 5),
            ('organizer', 6),
        )
        # with lookup
        for username, nevents in patterns:
            events = self._render_template(username, lookup='published')
            self.assertEqual(events.count(), nevents,
                             "{} should see {} events.".format(username,
                                                               nevents))
        # without lookup
        for username, nevents in patterns:
            events = self._render_template(username)
            self.assertEqual(events.count(), nevents,
                             "{} should see {} events.".format(username,
                                                               nevents))

    def test_get_events_draft(self):
        """get_events draft はユーザーが編集可能な下書きを返す"""
        patterns = (
            ('adam', 1),
            ('seele', 0),
            ('nerv', 0),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
            ('organizer', 1),
        )
        # with lookup
        for username, nevents in patterns:
            events = self._render_template(username, lookup='draft')
            self.assertEqual(events.count(), nevents,
                             "{} should see {} events.".format(username,
                                                               nevents))

    def test_get_events_active(self):
        """get_events active はユーザーが閲覧可能な非終了イベントを返す"""
        patterns = (
            ('adam', 5),
            ('seele', 5),
            ('nerv', 5),
            ('children', 5),
            ('wille', 4),
            ('anonymous', 4),
            ('organizer', 5),
        )
        # with lookup
        for username, nevents in patterns:
            events = self._render_template(username, lookup='active')
            self.assertEqual(events.count(), nevents,
                             "{} should see {} events.".format(username,
                                                               nevents))

    def test_get_events_attendable(self):
        """get_events attendable はユーザーが参加可能なイベントを返す"""
        patterns = (
            ('adam', 3),
            ('seele', 3),
            ('nerv', 3),
            ('children', 3),
            ('wille', 2),
            ('anonymous', 2),
            ('organizer', 3),
        )
        # with lookup
        for username, nevents in patterns:
            events = self._render_template(username, lookup='attendable')
            self.assertEqual(events.count(), nevents,
                             "{} should see {} events.".format(username,
                                                               nevents))

    def test_get_events_unknown(self):
        """get_events unknown はエラーを出す"""
        patterns = (
            ('adam', 0),
            ('seele', 0),
            ('nerv', 0),
            ('children', 0),
            ('wille', 0),
            ('anonymous', 0),
            ('organizer', 0),
        )
        # with lookup
        for username, nevents in patterns:
            self.assertRaises(TemplateSyntaxError, self._render_template,
                              username, lookup='unknown')
