__author__ = 'giginet'
import markdown2
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

register = template.Library()

class RenderMarkdown(template.Node):
    def __init__(self, template_path):
        self.template_path = template_path

    def render(self, context):
        template_path = template.resolve_variable(self.template_path, context)
        md = render_to_string(template_path)
        return mark_safe(markdown(md))


@register.tag
def render_markdown(parser, token):
    """
    テンプレートフォルダ以下にあるmarkdownを読み込んでレンダリングするテンプレートタグです
    主にroughpageでの使用を想定しています。
    Syntax:
        {% render_markdown "markdown/about.md" %}
    """
    bits = token.split_contents()
    if len(bits) != 2:
        raise template.TemplateSyntaxError("Syntax error. a correct syntax is '%s <template_path>'" % bits[0])
    return RenderMarkdown(bits[1])


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
        tables
            https://github.com/trentm/python-markdown2/wiki/tables
            GFMのテーブル記法を展開します
            これを使うにはPython-markdown2の2.3.0以上を使うこと！

    Usage:
        {{ object.body | markdown }}
    """
    md = markdown2.markdown(value, extras=['footnotes',
                                           'code-friendly',
                                           'tables'],
    )
    return mark_safe(md)

@register.tag(name="markdown")
def block_markdown(parser, token):
    nodelist = parser.parse(('endmarkdown'),)
    parser.delete_first_token()
    return MarkdownNode(nodelist)

class MarkdownNode(template.Node):
    """
    囲んだ部分をMarkdownとしてレンダリングするテンプレートタグです

    Usage:
        {% markdown %}
            かわずたん！ [Kawaz](http://www.kawaz.org/)
        {% endmarkdown %}
    """
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return markdown(output)
