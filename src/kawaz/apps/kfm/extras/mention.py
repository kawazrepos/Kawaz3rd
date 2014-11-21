# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import re
from django.template.loader import render_to_string
from .utils import is_quoated


PATTERN = re.compile(r'@(?P<username>[0-9a-zA-Z_\-]+)', flags=re.MULTILINE)
TEMPLATE_NAME = 'kfm/extras/mention.html'


def parse_mentions(value):
    """
    指定された文字列から @username という部分を探しリンク文字列に変換
    """
    from kawaz.core.personas.models import Persona
    usernames_specified = PATTERN.findall(value)
    # 指定されているユーザー限定でQuerySetを取得し変換用辞書を作成
    qs = Persona.objects.filter(username__in=usernames_specified)
    users = {u.username: u for u in qs}
    usernames_exists = users.keys()
    def repl(m):
        if is_quoated(m.string, m.start(), m.end()):
            # クォートされているので無視
            return m.group()
        username = m.group('username')
        if username in usernames_exists:
            html = render_to_string(TEMPLATE_NAME, {
                'user': users[username],
            })
            return html.strip()
        else:
            # 存在しないユーザーなので無視
            return m.group()
    value = PATTERN.sub(repl, value)
    return value
