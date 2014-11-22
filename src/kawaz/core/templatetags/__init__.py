# 一部template tagをbuilt in filter化します
from django.template import add_to_builtins
add_to_builtins('kawaz.core.templatetags.templatetags.expr')
add_to_builtins('kawaz.apps.kfm.templatetags.kfm')
