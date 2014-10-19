# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/20
#
from django_comments import CommentForm
from kawaz.core.forms.widgets import MaceEditorWidget

__author__ = 'giginet'

class KawazCommentForm(CommentForm):

    def __init__(self, *args, **kwargs):
        super(KawazCommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget = MaceEditorWidget()

