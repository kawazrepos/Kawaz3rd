from django import forms
from django.forms import ModelForm
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixin import Bootstrap3HorizontalFormHelperMixin

from .models import Entry

class EntryForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):

    body = forms.CharField(widget=MaceEditorWidget)

    class Meta:
        model = Entry
