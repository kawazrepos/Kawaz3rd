from django import template
from django.template import TemplateSyntaxError

register = template.Library()

class RenderWhenPatternThenNode(template.Node):
    def __init__(self, pattern, string):
        self.pattern = template.Variable(pattern)
        self.string = template.Variable(string)

    def render(self, context):
        pattern = self.pattern.resolve(context)
        string = self.string.resolve(context)
        import re
        request = context['request']
        if re.search(pattern, request.path):
            return string
        return ''


@register.tag
def when(parser, token):
    """

    """
    bits = token.split_contents()
    if not bits[1] == 'path' or \
            not bits[2] == '=~' or \
            not bits[4] == 'then' or \
                    len(bits) != 6:
        raise TemplateSyntaxError("This template tag must be 'when path =~ <pattern> then <string>'")
    return RenderWhenPatternThenNode(bits[3], bits[5])
