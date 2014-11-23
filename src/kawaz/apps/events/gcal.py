# coding=utf-8
"""
Google Calendar 連携用 Backend
`kawaz.core.google.calendar` に依存し settings.GOOGLE_CALENDAR_BACKEND で指定
されている
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.conf import settings
from django.contrib.sites.models import Site
from google_calendar.backend import Backend


def get_base_url():
    cache_name = '_cached_base_url'
    if not hasattr(get_base_url, cache_name):
        cs = Site.objects.get(pk=settings.SITE_ID)
        setattr(get_base_url, cache_name, 'http://{}'.format(cs))
    return getattr(get_base_url, cache_name)


class KawazGoogleCalendarBackend(Backend):
    def translate(self, event):
        """
        Kawaz3のEventモデルをGoogle Calendar API Version3のBodyパラメーターに変換します

        Params:
            event [Event] Eventモデルインスタンス
        Return:
            [dict] パラメーター
        """
        # translation lambda functions
        to_datetime = lambda x: {'dateTime': self.__class__.strftime(x)}
        to_visibility = lambda x: 'public' if x == 'public' else 'private'
        to_source = lambda x: {'url': get_base_url() + x()}
        to_attendees = lambda x: [dict(email=a.email, displayName=a.nickname)
                                  for a in x.iterator()]
        # translate
        translation_table = (
            ('summary', 'title', str),
            ('description', 'body', str),
            ('location', 'place', str),
            ('start', 'period_start', to_datetime),
            ('end', 'period_end', to_datetime),
            ('visibility', 'pub_state', to_visibility),
            ('source', 'get_absolute_url', to_source),
            ('attendees', 'attendees', to_attendees),
        )
        return {k: fn(getattr(event, a)) for k, a, fn in translation_table}

    def is_valid(self, event, raise_exception=False):
        """
        Kawaz3のEventモデルインスタンスが、Google Calendar API Version3の
        Bodyパラメーターと適合しているかをチェックします
        """
        if not event.period_start or not event.period_end:
            if raise_exception:
                raise AttributeError('`period_start` and `period_end` '
                                     'attributes are required to be filled.')
            return False
        elif event.pub_state == 'draft':
            if raise_exception:
                raise AttributeError('`pub_state` attribute is required not '
                                     'to be "draft".')
            return False
        return True
