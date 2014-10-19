# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/20
#
from django_comments import Comment
from kawaz.core.comments.forms import KawazCommentForm

__author__ = 'giginet'

def get_form():
    return KawazCommentForm

def get_model():
    return Comment
