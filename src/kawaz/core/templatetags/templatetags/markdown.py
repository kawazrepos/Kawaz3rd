__author__ = 'giginet'
import markdown2
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def markdown(value):
    """
    テキストをmarkdownに展開するtemplate filterです。
    processorとしてpython-markdown2を使っており、デフォルトの挙動の他に以下のExtrasを含めています

    kawaz.core.templatetagsでbuilt-in指定されています
    そのため、{% load markdown %}は不要です

    Notice:
        ブログパーツの使用などの利便性を持たせるために
        全てのHTMLタグを許可しています。
        セキュリティ上の懸念はありますが、このフィルタが適応されるのは
        Children権限以上のユーザーが作成したコンテンツのみであり
        本ポータルの性質から考えて悪用の可能性は少ないという判断です。

    Extras:
        footnotes
            https://github.com/trentm/python-markdown2/wiki/footnotes
            geekdrums [^foot-note]
            [^foot-note]: 神、いわゆるゴッド
        code-friendly
            https://github.com/trentm/python-markdown2/wiki/code-friendly
            _hello_, __yo__ などと言った記法を無効化します

    Usage:
        {{ object.body | markdown }}
    """
    md = markdown2.markdown(value, extras=['footnotes',
                                           'code-friendly'],
    )
    return mark_safe(md)
