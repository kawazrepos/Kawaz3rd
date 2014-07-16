from django import forms
from django.forms import ModelForm
from kawaz.core.forms.widgets import MaceEditorWidget

from .models import Entry

class EntryForm(ModelForm):

    body = forms.CharField(widget=MaceEditorWidget)

    class Meta:
        model = Entry
