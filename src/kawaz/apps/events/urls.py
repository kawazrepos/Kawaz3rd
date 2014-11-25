from django.conf.urls import patterns, include, url

from .views import EventListView, EventCreateView, EventDetailView, EventUpdateView, EventDeleteView, EventAttendView, EventQuitView, EventYearListView, EventMonthListView, EventPreviewView, EventCalendarView

urlpatterns = patterns('',
    url(r'^$', EventListView.as_view(), name='events_event_list'),
    url(r'^(?P<pk>\d+)/$', EventDetailView.as_view(), name='events_event_detail'),
    url(r'^(?P<pk>\d+)/calendar/$', EventCalendarView.as_view(), name='events_event_calendar'),
    url(r'^create/$', EventCreateView.as_view(), name='events_event_create'),
    url(r'^preview/$', EventPreviewView.as_view(), name='events_event_preview'),
    url(r'^(?P<pk>\d+)/update/$', EventUpdateView.as_view(), name='events_event_update'),
    url(r'^(?P<pk>\d+)/delete/$', EventDeleteView.as_view(), name='events_event_delete'),
    url(r'^(?P<pk>\d+)/attend/$', EventAttendView.as_view(), name='events_event_attend'),
    url(r'^(?P<pk>\d+)/quit/$', EventQuitView.as_view(), name='events_event_quit'),
    url(r'^archive/(?P<year>\d+)/$', EventYearListView.as_view(), name='events_event_archive-year'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/$',
        EventMonthListView.as_view(), name='events_event_archive_month'),
)
