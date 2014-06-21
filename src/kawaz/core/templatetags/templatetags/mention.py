import re
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from kawaz.core.personas.models import Persona

USERNAME_PATTERN = re.compile(r'@(?P<username>[0-9a-zA-Z-_]+)')

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def mention(value):
    """
    文中の@username にリンクを貼るテンプレートフィルタです
    """
    def repl(m):
        username = m.group('username')
        try:
            user = Persona.objects.get(username=username)
            html = render_to_string("templatetags/mention.html", {
                'user' : user
            }).replace('\n', '')
            return html
        except ObjectDoesNotExist:
            return "@{}".format(username)
    value = USERNAME_PATTERN.sub(repl, value)
    return mark_safe(value)
