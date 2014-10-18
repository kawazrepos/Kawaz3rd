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
    usernames = []
    for username in USERNAME_PATTERN.findall(value):
        usernames.append(username)
    users = Persona.objects.filter(username__in=usernames).values()
    users = {u['username']: u for u in users}
    print(users)
    def repl(m):
        username = m.group('username')
        if username in users.keys():
            html = render_to_string("templatetags/mention.html", {
                'user' : users[username]
            }).replace('\n', '')
            return html
        else:
            return "@{}".format(username)
    value = USERNAME_PATTERN.sub(repl, value)
    return mark_safe(value)
