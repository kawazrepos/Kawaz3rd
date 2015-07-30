# ! -*- coding: utf-8 -*-
#
#
#
from django_comments.forms import CommentForm
from django.utils.translation import ugettext_lazy as _
from kawaz.core.forms.fields import MarkdownField



class KawazCommentForm(CommentForm):
    comment = MarkdownField()

    def __init__(self, *args, **kwargs):
        super(KawazCommentForm, self).__init__(*args, **kwargs)

