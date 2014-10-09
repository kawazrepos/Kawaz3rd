from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin


from .models import Event

class EventForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):

    body = forms.CharField(label=_('Body'), widget=MaceEditorWidget)
    period_start = forms.DateTimeField(label=_('Start time'), widget=forms.DateTimeInput(attrs={'type': 'datetime'}), required=False)
    period_end = forms.DateTimeField(label=_('End time'), widget=forms.DateTimeInput(attrs={'type': 'datetime'}), required=False)
    attendance_deadline = forms.DateTimeField(label=_('Attendance deadline'),
                                              widget=forms.DateTimeInput(attrs={'type': 'datetime'}),
                                              required=False, help_text=Event._meta.get_field('attendance_deadline').help_text)

    class Meta:
        model = Event
        exclude = (
            'organizer',
            'created_at',
            'updated_at',
            'attendees',
        )
