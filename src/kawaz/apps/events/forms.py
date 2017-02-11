from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from kawaz.core.forms.fields import MarkdownField
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin
from kawaz.core.personas.forms.persona import PersonaChoiceField
from kawaz.core.personas.models import Persona
from .models import ATTENDANCE_DEADLINE_HELP_TEXT


from .models import Event


class EventForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):
    body = MarkdownField(label=_('Body'))
    period_start = forms.DateTimeField(label=_('Start time'),
                                       widget=forms.DateTimeInput(attrs={'type': 'datetime'}),
                                       required=False)
    period_end = forms.DateTimeField(label=_('End time'),
                                     widget=forms.DateTimeInput(attrs={'type': 'datetime'}),
                                     required=False)
    attendance_deadline = forms.DateTimeField(label=_('Attendance deadline'),
                                              widget=forms.DateTimeInput(attrs={'type': 'datetime'}),
                                              required=False, help_text=ATTENDANCE_DEADLINE_HELP_TEXT)

    class Meta:
        model = Event
        exclude = (
            'organizer',
            'created_at',
            'updated_at',
        )


class EventCreationForm(EventForm):
    class Meta:
        model = Event
        exclude = (
            'organizer',
            'created_at',
            'updated_at',
            'attendees'
        )


class EventUpdateForm(EventForm):
    attendees = PersonaChoiceField(
        label=_('Attendees'),
        queryset=Persona.objects.filter(is_active=True).order_by('pk'),
        help_text=_('Add attendees of this event'))