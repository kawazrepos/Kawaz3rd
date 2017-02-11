# ! -*- coding: utf-8 -*-
#
#
#
from django import forms
from django_comments.forms import CommentForm
from kawaz.core.forms.fields import MarkdownField



class KawazCommentForm(CommentForm):
    name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    comment = MarkdownField()

    def __init__(self, *args, **kwargs):
        super(KawazCommentForm, self).__init__(*args, **kwargs)

