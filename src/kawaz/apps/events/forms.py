from django import forms
from django.forms import ModelForm
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.crispy import Bootstrap3HorizontalFormMixin

from .models import Event

class EventForm(Bootstrap3HorizontalFormMixin, ModelForm):

    body = forms.CharField(widget=MaceEditorWidget)
    period_start = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime'}), required=False)
    period_end = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime'}), required=False)
    attendance_deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime'}), required=False)

    class Meta:
        model = Event
