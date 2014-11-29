import markdown2
from .extras.youtube import parse_youtube_urls
from .extras.nicovideo import parse_nicovideo_urls
from .extras.mention import parse_mentions
from .extras.strikethrough import parse_strikethroughs
from .extras.autolink import parse_autolinks



_markdown = markdown2.Markdown(extras=[
    'cuddled-lists',        # リスト記法でパラグラフの分断を可能に
    'code-friendly',        # _, __ による em, strong を無効化
    'fenced-code-blocks',   # ``` で囲まれた部分をソースコードとして扱う
    'footnotes',            # 脚注シンタックス（[^label]）を追加
    'tables',               # GFM的なテーブルシンタックスを追加
])


def parse_kfm(value):
    """
    Kawaz Flavored Markdown のパースを行いHTMLを返す

    kfm は下記の機能を提供する

    -   GitHub Flavored Markdown (2014) と等価の Markdown 機能
        -   Multiple underscores in words
        -   URL autolinking
        -   Strikethrough
        -   Fenced code blocks
        -   Syntax highlighting
        -   Tables
    -   脚注シンタックスの追加
    -   Cuddled Lists (パラグラフ直下でもリスト記法が有効）
    -   YouTube URL のプレイヤー展開
    -   ニコニコ動画URLのプレイヤー展開
    -   @username のユーザーリンク展開 (Kawaz ユーザー)
    -   {attachment: <slug>} の添付展開
    """
    from kawaz.apps.attachments.templatetags.attachments import (
        parse_attachments
    )
    # Kawaz独自機能
    value = parse_mentions(value)
    value = parse_attachments(value)
    # GitHub Flavored Markdown + Alpha
    value = _markdown.convert(value)
    value = parse_strikethroughs(value)
    # Markdownが提要されていないURLのプレイヤー展開
    value = parse_youtube_urls(value)
    value = parse_nicovideo_urls(value)
    # プレイヤー展開が適用されていないURLのリンク展開
    value = parse_autolinks(value)
    return value.strip()
