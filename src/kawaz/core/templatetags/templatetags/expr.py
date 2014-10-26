# ref: https://djangosnippets.org/snippets/9/
import re
from django import template
from django.utils.translation import ugettext_lazy

register = template.Library()


class ExprNode(template.Node):
    def __init__(self, expression, variable=None):
        self.expression = expression
        self.variable = variable

    def render(self, context):
        d = {'_': ugettext_lazy}
        for x in iter(context):
            d.update(x)
        if self.variable:
            context[self.variable] = eval(self.expression, d)
            return ''
        else:
            return str(eval(self.expression, d))


expr_r = re.compile(r'(.*?)\s+as\s+(\w+)', re.DOTALL)

@register.tag('expr')
def do_expr(parser, token):
    """
    テンプレート内でPythonの機能を実行し描画 or 変数代入するタグ

    Syntax:
        {% expr <expression> (as <variable) %}

    Example:
        {# 2 を描画 #}
        {% expr 1 + 1 %}
        {# 10 を foo に代入 #}
        {% expr 1 + 9 as foo %}
        {# foo を使って掛け算し描画 #}
        {% expr foo * 100 %}
    """
    bits = token.contents.split(None, 1)
    if len(bits) < 2:
        raise template.TemplateSyntaxError(
            "%r tag requires argument" % bits[0]
        )
    m = expr_r.search(bits[1])
    if m:
        expression, variable = m.groups()
    else:
        expression, variable = bits[1], None
    return ExprNode(expression, variable)
