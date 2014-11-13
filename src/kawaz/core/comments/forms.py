# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/20
#
from django_comments import CommentForm
from django.utils.translation import ugettext_lazy as _
from kawaz.core.forms.fields import MarkdownField

__author__ = 'giginet'

class KawazCommentForm(CommentForm):
    comment = MarkdownField()

    def __init__(self, *args, **kwargs):
        super(KawazCommentForm, self).__init__(*args, **kwargs)

