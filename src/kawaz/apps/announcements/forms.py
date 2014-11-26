from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from kawaz.core.forms.fields import MarkdownField
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin
from .models import Announcement


class AnnouncementForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):

    body = MarkdownField(label=_('Body'))

    class Meta:
        model = Announcement
        exclude = (
            'author',
            'created_at',
            'updated_at',
        )
