# 一部template tagをbuilt in filter化します
from django.template import add_to_builtins
add_to_builtins('kawaz.core.templatetags.templatetags.markdown')
add_to_builtins('kawaz.core.templatetags.templatetags.expr')
