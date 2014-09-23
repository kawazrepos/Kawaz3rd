from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import urlize

from .embed import youtube, nicovideo
from .mention import mention
from .markdown import markdown
from kawaz.apps.attachments.templatetags.attachments import parse_attachments

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def parser(value):
    """
    Kawazで使用するtemplate tagsをまとめて使用するtemplate filterです
    以下の処理を行います
        YouTube展開
            YouTubeの動画URLをプレーヤーとして展開します
            ref: kawaz.core.templatetags.tempaltetags.embed.youtube
        ニコニコ動画展開
            ニコニコ動画の動画URLをプレーヤーとして展開します
            ref: kawaz.core.templatetags.tempaltetags.embed.nicovideo
        URLをリンクに展開
            URLやメールアドレスの文字列をリンクタグに変換します
            ref: django.template.defaultfilters.urlize
        @usernameを展開
            @username という文字列をユーザーへのリンクタグに変換します
            ref: kawaz.core.templatetags.tempaltetags.mention.mention
        markdown展開
            markdownをHTMLに展開します
            ref: kawaz.core.templatetags.tempaltetags.markdown.markdown
        添付ファイル展開
            {attachments:<slug>}をファイル埋め込みに展開します
            ref: kawaz.apps.attachments.templatetags.attachments.parse_attachments
    """
    # Youtube, NicoNico
    value = youtube(value)
    value = nicovideo(value)
    # URL
    value = urlize(value)
    # @言及
    value = mention(value)
    # markdown
    value = markdown(value)
    # 添付ファイル展開
    value = parse_attachments(value)
    return mark_safe(value)