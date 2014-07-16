from django import forms
from django.forms import ModelForm
from kawaz.core.forms.widgets import MaceEditorWidget

from .models import Event

class EventForm(ModelForm):

    body = forms.CharField(widget=MaceEditorWidget)
    period_start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime'}))
    period_end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime'}))
    attendance_deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime'}))

    class Meta:
        model = Event
