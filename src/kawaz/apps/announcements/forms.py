from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext as _
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin

from .models import Announcement

class AnnouncementForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):

    body = forms.CharField(label=_('Body'), widget=MaceEditorWidget)

    class Meta:
        model = Announcement
        exclude = (
            'author',
            'created_at',
            'updated_at',
        )
