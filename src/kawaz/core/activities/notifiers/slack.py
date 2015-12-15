import urllib
import json
import re
import itertools
from django.conf import settings
from activities.notifiers.base import ActivityNotifierBase

DEFAULT_USERNAME = 'Kawaz'
DEFAULT_ICON_EMOJI = ':frog:'


class SlackActivityNotifier(ActivityNotifierBase):
    """
    ActivityをSlackの特定のチャンネルに通知します。settings.pyに以下の項目を追加する必要があります。

    Setting
        ACTIVITIES_ENABLE_SLACK_NOTIFICATION [boolean]
            Slack通知を有効にするかどうかを設定します

        ACTIVITES_INSTALLED_NOTIFIERS
            以下のようなパラメータを設定してください
            各パラメーターの詳細についてはSlackのAPIドキュメントを参照してください
            https://api.slack.com/incoming-webhooks
            第3引数 [String]
                Slack Incomming-WebHooks URL
            第4引数 [String]
                Slackで通知を有効にするチャンネル名です
            第5引数 [Dict]
                username
                    Slack上の通知名です。設定しない場合はデフォルト値が利用されます
                icon_emoji
                    Slack上のアイコンに使う絵文字のIDです。
                    icon_urlが設定されている場合はそちらが優先されます
                icon_url
                    Slack上のアイコンに使う画像のURLです

        >>> ACTIVITIES_INSTALLED_NOTIFIERS = (
        >>>    ('slack_kawaz_all',
        >>>    'kawaz.core.activities.notifiers.slack.SlackActivityNotifier',
        >>>    'https://kawaz.slack.com/token',
        >>>    '#general',
        >>>    {'username': 'かわずたん', 'icon_emoji': ':beer:'})
        >>> )
    """
    typename = 'slack'
    TAG_PATTERN = re.compile(r'<(?P<key>[a-z_]+)=(?P<value>.+)>')

    def __init__(self, url, channel, params={}):
        self.url = url
        self.channel = channel
        self.icon_emoji = params.get('icon_emoji', DEFAULT_ICON_EMOJI)
        self.default_username = params.get('username', DEFAULT_USERNAME)
        self.default_icon_url = params.get('icon_url', '')

    def send(self, rendered_content):
        if not settings.ACTIVITIES_ENABLE_SLACK_NOTIFICATION:
            return
        message, params = self._parse_content(rendered_content)
        username = params.get('username', self.default_username)
        icon_url = params.get('icon_url', self.default_icon_url)
        params = {
            'text': message,
            'channel': self.channel,
            'username': username,
            'icon_emoji': self.icon_emoji,
            'icon_url': icon_url
        }
        payload = {'payload': json.dumps(params)}
        data = urllib.parse.urlencode(payload)
        data = data.encode('utf-8')
        request = urllib.request.Request(self.url, data)
        urllib.request.urlopen(request)

    def _parse_content(self, rendered_content):
        valid_tags = ('username', 'icon_url')
        params = {}
        lines = rendered_content.split('\n')
        for line in lines:
            match = self.TAG_PATTERN.match(line)
            if not match:
                break
            key = match.group('key')
            value = match.group('value')
            if key in valid_tags:
                params.update({key: value})

        bodies = itertools.dropwhile(lambda text: self.TAG_PATTERN.match(text), lines)
        message = '\n'.join(bodies)
        return message, params
