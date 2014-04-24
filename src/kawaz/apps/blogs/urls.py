from django.conf.urls import patterns, include, url

from .views import EntryAuthorDayArchiveView
from .views import EntryAuthorListView
from .views import EntryAuthorMonthArchiveView
from .views import EntryAuthorTodayArchiveView
from .views import EntryAuthorYearArchiveView
from .views import EntryCreateView
from .views import EntryDayArchiveView
from .views import EntryDeleteView
from .views import EntryDetailView
from .views import EntryListView
from .views import EntryMonthArchiveView
from .views import EntryTodayArchiveView
from .views import EntryUpdateView
from .views import EntryYearArchiveView

author_patterns = patterns('',
   url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<pk>\d+)/$', EntryDetailView.as_view(), name='blogs_entry_detail'),
   url(r'^create/$', EntryCreateView.as_view(), name='blogs_entry_create'),
   url(r'^(?P<pk>\d+)/update/$', EntryUpdateView.as_view(), name='blogs_entry_update'),
   url(r'^(?P<pk>\d+)/delete/$', EntryDeleteView.as_view(), name='blogs_entry_delete'),
   url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', EntryAuthorDayArchiveView.as_view(), name='blogs_entry_author_archive-day'),
   url(r'^(?P<year>\d+)/(?P<month>\d+)/$', EntryAuthorMonthArchiveView.as_view(), name='blogs_entry_author_archive-month'),
   url(r'^(?P<year>\d+)/$', EntryAuthorYearArchiveView.as_view(), name='blogs_entry_author_archive-year'),
   url(r'^today/$', EntryAuthorTodayArchiveView.as_view(), name='blogs_entry_author_archive-today'),
   url(r'^$', EntryAuthorListView.as_view(), name='blogs_author_entry_list'),
)

urlpatterns = patterns('',
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', EntryDayArchiveView.as_view(), name='blogs_entry_archive-day'),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', EntryMonthArchiveView.as_view(), name='blogs_entry_archive-month'),
    url(r'^(?P<year>\d+)/$', EntryYearArchiveView.as_view(), name='blogs_entry_archive-year'),
    url(r'^$', EntryListView.as_view(), name='blogs_entry_list'),
    url(r'^today/$', EntryTodayArchiveView.as_view(), name='blogs_entry_archive-today'),
    (r'^(?P<author>\w+)/', include(author_patterns)),
)