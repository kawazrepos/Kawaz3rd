# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import re
from django.template.loader import render_to_string
from .utils import is_quoated


PATTERN = re.compile(
    r"https?://www\.nicovideo\.jp/watch/(?P<id>[a-zA-Z0-9_\-]+)/?",
    flags=re.MULTILINE,
)
TEMPLATE_NAME = 'kfm/extras/nicovideo.html'


def parse_nicovideo_urls(value):
    """
    指定された文字列に含まれる ニコニコ動画 URL をプレイヤーに変換
    ただしURLがシングル・ダブルクオーテーションマークで囲まれていた場合は
    変換を行わない

    変換にはテンプレートシステムが使用され `kfm/parsers/nicovideo.html`
    なおコンテキストとして下記の値がテンプレートに渡される

    -   video_id: ニコニコ動画 ID

    """
    def repl(m):
        if is_quoated(m.string, m.start(), m.end()):
            # ', " に囲まれているため置換を行わない
            return m.group()
        params = dict(
            video_id=m.group('id'),
        )
        html = render_to_string(TEMPLATE_NAME, params)
        return html.strip()
    value = PATTERN.sub(repl, value)
    return value
