# ! -*- coding: utf-8 -*-
#
#
#
from django_comments.models import Comment
from kawaz.core.comments.forms import KawazCommentForm



def get_form():
    return KawazCommentForm

def get_model():
    return Comment
