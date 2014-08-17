from django import forms
from django.forms import ModelForm
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.crispy import Bootstrap3HorizontalFormMixin

from .models import Entry

class EntryForm(Bootstrap3HorizontalFormMixin, ModelForm):

    body = forms.CharField(widget=MaceEditorWidget)

    class Meta:
        model = Entry
