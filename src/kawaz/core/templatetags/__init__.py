#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/9
#
__author__ = 'giginet'
# 一部template tagをbuilt in filter化します
from django.template import add_to_builtins
add_to_builtins('kawaz.core.templatetags.templatetags.markdown')
