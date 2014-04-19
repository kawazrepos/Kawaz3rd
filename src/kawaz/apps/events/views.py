from django.views.generic.detail import DetailView
from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.edit import ModelFormMixin, CreateView, UpdateView, DeleteView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed

from permission.decorators import permission_required

from kawaz.core.views.decorators import class_view_decorator
from .models import Event
from .forms import EventForm

class EventQuerySetMixin(MultipleObjectMixin):
    def get_queryset(self):
        return Event.objects.published(self.request.user)


class EventSetOrganizerMixin(ModelFormMixin):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            data = kwargs['data'].copy()
            data['organizer'] = str(self.request.user.pk)
            kwargs['data'] = data
        return kwargs

class EventListView(ListView, EventQuerySetMixin):
    model = Event


@permission_required('events.view_event')
class EventDetailView(DetailView):
    model = Event


@class_view_decorator(login_required)
class EventCreateView(CreateView, EventSetOrganizerMixin):
    model = Event
    form_class = EventForm


@permission_required('events.change_event')
class EventUpdateView(UpdateView, EventSetOrganizerMixin):
    model = Event
    form_class = EventForm


@permission_required('events.delete_event')
class EventDeleteView(DeleteView):
    model = Event
    success_url = reverse_lazy('events_event_list')


@permission_required('event.attend_event')
class EventJoinView(UpdateView):
    model = Event
    success_url = reverse_lazy('events_event_list')

    def attend(self, request, *args, **kwargs):
        """
        Calls the attend() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.attend(request.user)
            return HttpResponseRedirect(success_url)
        except PermissionDenied:
            return HttpResponseForbidden

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed()

    def post(self, request, *args, **kwargs):
        return self.attend(request, *args, **kwargs)


@permission_required('events.quit_event')
class EventQuitView(UpdateView):
    model = Event
    success_url = reverse_lazy('events_event_list')

    def quit(self, request, *args, **kwargs):
        """
        Calls the attend() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.quit(request.user)
            return HttpResponseRedirect(success_url)
        except PermissionDenied:
            return HttpResponseForbidden

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed()

    def post(self, request, *args, **kwargs):
        return self.quit(request, *args, **kwargs)


class EventYearListView(YearArchiveView, EventQuerySetMixin):
    model = Event
    date_field = 'period_start'


class EventMonthListView(MonthArchiveView, EventQuerySetMixin):
    model = Event
    date_field = 'period_start'


class EventDayListView(DayArchiveView, EventQuerySetMixin):
    model = Event
    date_field = 'period_start'