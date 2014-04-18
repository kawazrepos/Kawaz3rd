from django.conf.urls import patterns, include, url

from .views import EventListView, EventCreateView, EventDetailView, EventUpdateView, EventDeleteView, EventJoinView, EventQuitView, EventYearListView, EventMonthListView, EventDayListView

urlpatterns = patterns('',
    url(r'^$', EventListView.as_view(), name='events_event_list'),
    url(r'^(?P<pk>\d+)/$', EventDetailView.as_view(), name='events_event_detail'),
    url(r'^create/$', EventCreateView.as_view(), name='events_event_create'),
    url(r'^(?P<pk>\d+)/update/$', EventUpdateView.as_view(), name='events_event_update'),
    url(r'^(?P<pk>\d+)/delete/$', EventDeleteView.as_view(), name='events_event_delete'),
    url(r'^(?P<pk>\d+)/join/$', EventJoinView.as_view(), name='events_event_join'),
    url(r'^(?P<pk>\d+)/quit/$', EventQuitView.as_view(), name='events_event_quit'),
    url(r'^(?P<pk>\d+)/quit/(?P<user>[^/]+)/$', EventQuitView.as_view(), name='events_event_quit'),
    url(r'^archive/(?P<year>\d+)/$', EventYearListView.as_view(), name='events_event_archive-year'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/$',
        EventMonthListView.as_view(), name='events_event_archive_month'),
    url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        EventDayListView, name='events_event_archive-day'),
)
