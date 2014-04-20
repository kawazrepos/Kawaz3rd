from django.views.generic.detail import DetailView
from django.views.generic.list import ListView, MultipleObjectMixin
from django.views.generic.edit import ModelFormMixin, CreateView, UpdateView, DeleteView
from django.views.generic.dates import YearArchiveView, MonthArchiveView, BaseArchiveIndexView
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseRedirect, HttpResponseForbidden, HttpResponseNotAllowed

from permission.decorators import permission_required

from .models import Event
from .forms import EventForm

class EventPublishedQuerySetMixin(MultipleObjectMixin):
    def get_queryset(self):
        return Event.objects.published(self.request.user).order_by()


class EventActiveQuerySetMixin(MultipleObjectMixin):
    def get_queryset(self):
        return Event.objects.active(self.request.user)

class EventDateArchiveMixin(BaseArchiveIndexView):
    def get(self, request, *args, **kwargs):
        self.date_list, self.object_list, extra_context = self.get_dated_items()
        self.object_list = self.object_list.order_by('period_start') # 日付昇順にならない
        context = self.get_context_data(object_list=self.object_list,
                                        date_list=self.date_list)
        context.update(extra_context)
        return self.render_to_response(context)

class EventSetOrganizerMixin(ModelFormMixin):
    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

class EventListView(ListView, EventActiveQuerySetMixin):
    model = Event


@permission_required('events.view_event')
class EventDetailView(DetailView):
    model = Event


@permission_required('events.add_event')
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
class EventAttendView(UpdateView):
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


class EventYearListView(YearArchiveView, EventPublishedQuerySetMixin, EventDateArchiveMixin):
    model = Event
    date_field = 'period_start'
    allow_empty = True
    allow_future = True
    make_object_list = True
    paginate_by = 10


class EventMonthListView(MonthArchiveView, EventPublishedQuerySetMixin, EventDateArchiveMixin):
    model = Event
    date_field = 'period_start'
    allow_empty = True
    allow_future = True
    month_format = '%m'

