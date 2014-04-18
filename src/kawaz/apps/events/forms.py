from django import forms
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.contrib.auth import get_user_model

from .models import Event

class EventForm(ModelForm):
    organizer = forms.ModelChoiceField(queryset=get_user_model().objects.all(), widget=HiddenInput())
    class Meta:
        model = Event
        exclude = ['body_markup_type']
