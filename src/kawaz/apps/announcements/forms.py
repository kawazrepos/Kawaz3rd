from django.forms import ModelForm
from django import forms
from kawaz.core.forms.widgets import MaceEditorWidget

from .models import Announcement

class AnnouncementForm(ModelForm):

    body = forms.CharField(widget=MaceEditorWidget)

    class Meta:
        model = Announcement
