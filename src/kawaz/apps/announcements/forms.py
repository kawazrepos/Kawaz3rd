from django.forms import ModelForm
from django import forms
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin

from .models import Announcement

class AnnouncementForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):

    body = forms.CharField(label=Announcement._meta.get_field('body').verbose_name, widget=MaceEditorWidget)

    class Meta:
        model = Announcement
        exclude = (
            'author',
            'created_at',
            'updated_at',
        )
