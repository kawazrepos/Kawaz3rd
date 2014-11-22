from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from kawaz.core.forms.fields import MarkdownField
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin
from .models import ATTENDANCE_DEADLINE_HELP_TEXT


from .models import Event

class EventForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):

    body = MarkdownField(label=_('Body'))
    period_start = forms.DateTimeField(label=_('Start time'), widget=forms.DateTimeInput(attrs={'type': 'datetime'}), required=False)
    period_end = forms.DateTimeField(label=_('End time'), widget=forms.DateTimeInput(attrs={'type': 'datetime'}), required=False)
    attendance_deadline = forms.DateTimeField(label=_('Attendance deadline'),
                                              widget=forms.DateTimeInput(attrs={'type': 'datetime'}),
                                              required=False, help_text=ATTENDANCE_DEADLINE_HELP_TEXT)

    class Meta:
        model = Event
        exclude = (
            'organizer',
            'created_at',
            'updated_at',
            'attendees',
        )
