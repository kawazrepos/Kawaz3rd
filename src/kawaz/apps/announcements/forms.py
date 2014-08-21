from django.forms import ModelForm
from django import forms
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin

from .models import Announcement

class AnnouncementForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):

    body = forms.CharField(widget=MaceEditorWidget)

    class Meta:
        model = Announcement
