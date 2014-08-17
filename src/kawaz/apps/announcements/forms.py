from django.forms import ModelForm
from django import forms
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixin import Bootstrap3HorizontalFormMixin

from .models import Announcement

class AnnouncementForm(Bootstrap3HorizontalFormMixin, ModelForm):

    body = forms.CharField(widget=MaceEditorWidget)

    class Meta:
        model = Announcement
