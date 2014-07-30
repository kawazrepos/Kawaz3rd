# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/7/28
#
__author__ = 'giginet'
from django.conf import settings
from django.contrib.sites.models import Site
import httplib2

from apiclient import discovery
from oauth2client import file

STRFTIME_FORMAT = '%Y-%m-%dT%H:%M:%S.000%z'

class GoogleCalendarUpdater(object):
    """
    EventをGoogleカレンダーと同期するための操作をまとめたクラスです
    主にEvent更新、削除時のSignalとして呼ばれることを想定しています
    """

    def __init__(self):
        self.service = None
        if not settings.GOOGLE_CALENDAR_ID:
            return
        try:
            self.service = self._login()
        except:
            pass

    def body_from_event(self, event):
        """
        Eventオブジェクトから、Google Calendar API V3に送信するためのJSONを作ります
        詳細は以下のドキュメントを参考にしてください
            Ref : https://developers.google.com/google-apps/calendar/v3/reference/events/insert

        param event [Event] Eventインスタンス
        return [Dictionary]
        """
        if not event.period_start or not event.period_end:
            raise Exception("Event instance must be have `period_start` and `period_end`.")
        current_site = Site.objects.get(pk=settings.SITE_ID)
        base_url = 'http://{}'.format(current_site)


        body = {
            'summary': event.title,
            'description': event.body,
            'location': event.place,
            'start': {
                'dateTime': event.period_start.strftime(STRFTIME_FORMAT)
            },
            'end': {
                'dateTime': event.period_end.strftime(STRFTIME_FORMAT)
            },
            'visibility': 'public' if event.pub_state == 'public' else 'private',
            'source': {
                'url':  base_url + event.get_absolute_url()
            },
            'attendees':[]
        }

        for attendee in event.attendees.all():
            user = {
                'email': attendee.email,
                'displayName': attendee.nickname
            }
            body['attendees'].append(user)
        return body

    def _login(self):
        """
         oAuth2で取得したACCESS_TOKENを利用してGoogleにログインします
         このメソッドを実行する前に、必ず`python manage.py login_to_google`を実行し、
         `GOOGLE_CREDENTIALS_PATH`に認証情報が保存されている必要があります
        """
        storage_path = settings.GOOGLE_CREDENTIALS_PATH

        storage = file.Storage(storage_path)
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            raise Exception("You must execute `python manage.py login_to_google` to fetch access_token.")
        http = credentials.authorize(http = httplib2.Http())

        service = discovery.build('calendar', 'v3', http=http)
        return service

    def update_event(self, instance, created):
        """
        EventをGoogle Calendarと同期します

        param instance [Event] 同期するEventオブジェクト
        param created [Boolean] 新規作成かどうか

        もし、Googleカレンダーにイベントが存在していなければ新規作成します
        すでに作られていて、編集されていれば更新します。
        すでに作られているが、開催日が未定になったり、下書き状態に切り替わっていたとき、削除します
        """
        if not self.service:
            return
        if not instance.period_start or not instance.period_end or instance.pub_state == 'draft':
            # 開始日、終了日が設定されていない、もしくは下書き状態のイベントは無視する
            if instance.gcal_id:
                # もしカレンダー同期設定済みだったら、削除する
                self.delete_event(instance)
                instance.gcal_id = ''
                instance.save()
            return

        kwargs = {}
        if instance.number_restriction:
            # もし、最大人数が設定されてたら、maxAttendeesを指定する
            kwargs['maxAttendees']

        if created or not instance.gcal_id:
            # 新規作成、もしくは同期されていなかったとき
            body = self.body_from_event(instance)
            try:
                created_event = self.service.events().insert(calendarId=settings.GOOGLE_CALENDAR_ID, body=body, **kwargs).execute()
                instance.gcal_id = created_event['id']
                instance.save()
            except:
                pass
        else:
            # 更新するとき
            gcal_id = instance.gcal_id
            body = self.body_from_event(instance)
            try:
                # updateじゃなくてpatchを使うべきらしい
                # http://stackoverflow.com/questions/15926676/google-calendar-api-bad-request-400-event-over-developer-console
                self.service.events().patch(calendarId=settings.GOOGLE_CALENDAR_ID, eventId=gcal_id, body=body, **kwargs).execute()
            except:
                pass

    def delete_event(self, instance):
        """
        渡されたEventをGoogle Calendarから削除します

        param instance [Event] 削除するEventオブジェクト
        """
        if not self.service:
            return
        if instance.gcal_id:
            return
        try:
            self.service.events().delete(calendarId=settings.GOOGLE_CALENDAR_ID, eventId=instance.gcal_id).execute()
        except:
            return
