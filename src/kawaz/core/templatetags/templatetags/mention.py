import re
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from kawaz.core.personas.models import Persona

USERNAME_PATTERN = r'@(?P<username>[0-9a-zA-Z-_]+)'

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def mention(value):
    """
    文中の@username にリンクを貼るテンプレートフィルタです
    """
    regex = re.compile(USERNAME_PATTERN)
    def repl(m):
        username = m.group('username')
        try:
            user = Persona.objects.get(username=username)
            html = render_to_string("templatetags/mention.html", {
                'user' : user
            })
            return html
        except ObjectDoesNotExist:
            return "@{}".format(username)
    value = regex.sub(repl, value)
    return mark_safe(value)
