# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import re
from django.template.loader import render_to_string
from .utils import is_quoated


PATTERN = re.compile(
    r"https?://www\.youtube\.com/watch\?v=(?P<id>[a-zA-Z0-9_\-]+)"
)
TEMPLATE_NAME = r"kfm/extras/youtube.html"

DEFAULT_WIDTH = 640
DEFAULT_HEIGHT = 360
ASPECT_RATIO = 16.0 / 9.0


def parse_youtube_urls(value, responsive=False, width=None, height=None):
    """
    指定された文字列に含まれる YouTube URL をプレイヤーに変換
    ただしURLがシングル・ダブルクオーテーションマークで囲まれていた場合は
    変換を行わない

    変換にはテンプレートシステムが使用され `kfm/parsers/youtube.html`
    なおコンテキストとして下記の値がテンプレートに渡される

    -   video_id: YouTube Video ID
    -   responsive: レスポンシブデザインで描画すべきか否か
    -   width: 横幅（responsiveには渡されない）
    -   height: 縦幅（responsiveには渡されない）

    Args:
        responsive (bool): bootstrapのレスポンシブデザインに対応させる
            http://getbootstrap.com/components/#responsive-embed
            これが指定された場合下記 width/height の指定は無視される
        width (int or None): 横幅 (px) 指定されない場合は DEFAULT_WIDTH
            が使用される
        height (int or None): 縦幅 (px) 指定されない場合は width に対して
            アスペクト比が 16:9 に成るように自動指定される
    """
    if responsive == False:
        if width is None:
            width = DEFAULT_WIDTH
        if height is None:
            height = width / ASPECT_RATIO
        # width/height は整数値
        width = int(width)
        height = int(height)

    def repl(m):
        if is_quoated(m.string, m.start(), m.end()):
            # ', " に囲まれているため置換を行わない
            return m.group()
        params = dict(
            video_id=m.group('id'),
            responsive=responsive,
            width=width,
            height=height,
        )
        html = render_to_string(TEMPLATE_NAME, params)
        return html.strip()
    value = PATTERN.sub(repl, value)
    return value
