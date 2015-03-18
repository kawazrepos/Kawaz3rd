import urllib
from django.conf import settings
from activities.notifiers.base import ActivityNotifierBase

__author__ = 'giginet'

HIPCHAT_API_BASE = 'https://api.hipchat.com/'
MESSAGE_END_POINT = 'v1/rooms/message'
DEFAULT_COLOR = 'random'
DEFAULT_FROM_NAME = 'Kawaz'

class HipChatActivityNotifier(ActivityNotifierBase):
    """
    ActivityをHipChatの特定のルームに通知します。settings.pyに以下の項目を追加する必要があります。

    Setting
        ACTIVITIES_ENABLE_HIPCHAT_NOTIFICATION [boolean]
            HipChat通知を有効にするかどうかを設定します

        ACTIVITES_INSTALLED_NOTIFIERS
            以下のようなパラメータを設定してください
            第3引数 [String]
                HipChat API用のAuthトークンです。
            第4引数 [String]
                HipChat上で通知を有効にする部屋IDです
            第5引数 [Dict]
                from
                    HipChat上の通知名です。設定しない場合はデフォルト値が利用されます。
                color
                    HipChat上の表示色です。設定しない場合はランダム値が設定されます。
                    設定値はHipChat APIに準拠します。
                notify
                    通知があったとき、ルームメンバーに通知するかを設定します。
                    デフォルトでは常に通知します。

        >>> ACTIVITIES_INSTALLED_NOTIFIERS = (
        >>>    ('hipchat_kawaz_all',
        >>>    'kawaz.core.activities.notifiers.hipchat.HipChatActivityNotifier',
        >>>    'mytoken',
        >>>    'roomid',
        >>>    {'from_name': 'Kawazポータル', 'color': 'green', 'is_notify': True})
        >>> )
    """
    typename = 'hipchat'

    def __init__(self, auth_token, room_id, params={}):
        self.auth_token = auth_token
        self.room_id = room_id
        self.color = params.get('color', DEFAULT_COLOR)
        self.from_name = params.get('from_name', DEFAULT_FROM_NAME)
        self.is_notify = params.get('is_notify', True)

    def send(self, rendered_content):
        if not settings.ACTIVITIES_ENABLE_HIPCHAT_NOTIFICATION:
            return
        params = {
            'format': 'json',
            'color': self.color,
            'message': rendered_content,
            # HipChat API v1.0では1か0で指定する
            # https://www.hipchat.com/docs/api/method/rooms/message
            'notify': 1 if self.is_notify else 0,
            'message_format': 'html',
            'from': self.from_name,
            'room_id': self.room_id,
            'auth_token': self.auth_token
        }

        url = urllib.parse.urljoin(HIPCHAT_API_BASE, MESSAGE_END_POINT)
        data = urllib.parse.urlencode(params)
        data = data.encode('utf-8')
        request = urllib.request.Request(url, data)
        urllib.request.urlopen(request)
