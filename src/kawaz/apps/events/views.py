from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView
from django.contrib.auth.decorators import login_required

from permission.decorators import permission_required

from .models import Event

class EventListView(ListView):
    model = Event

@permission_required('event.view_event')
class EventDetailView(DetailView):
    model = Event

class EventCreateView(CreateView):
    model = Event

@permission_required('event.change_event')
class EventUpdateView(UpdateView):
    model = Event

@permission_required('event.delete_event')
class EventDeleteView(DeleteView):
    model = Event

@permission_required('event.attend_event')
class EventJoinView(UpdateView):
    model = Event

@permission_required('event.quit_event')
class EventQuitView(UpdateView):
    model = Event

class EventYearListView(YearArchiveView):
    model = Event
    date_field = 'period_start'

class EventMonthListView(MonthArchiveView):
    model = Event
    date_field = 'period_start'

class EventDayListView(DayArchiveView):
    model = Event
    date_field = 'period_start'

