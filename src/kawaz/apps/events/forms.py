from django import forms
from django.forms import ModelForm
from django.forms.widgets import HiddenInput
from django.contrib.auth import get_user_model

from .models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
