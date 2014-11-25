from django.conf.urls import patterns, url

from .views import ProjectListView, ProjectPreviewView
from .views import ProjectUpdateView
from .views import ProjectCreateView
from .views import ProjectDeleteView
from .views import ProjectDetailView
from .views import ProjectJoinView
from .views import ProjectQuitView
from .views import ProjectArchiveView


urlpatterns = patterns('',
    url('^$',
        ProjectListView.as_view(), name='projects_project_list'),
    url('^create/$',
        ProjectCreateView.as_view(), name='projects_project_create'),
    url('^preview/$',
        ProjectPreviewView.as_view(), name='projects_project_preview'),
    url('^archives/$',
        ProjectArchiveView.as_view(), name='projects_project_archives'),
    url('^(?P<pk>\d+)/update/$',
        ProjectUpdateView.as_view(), name='projects_project_update'),
    url('^(?P<pk>\d+)/join/$',
        ProjectJoinView.as_view(), name='projects_project_join'),
    url('^(?P<pk>\d+)/quit/$',
        ProjectQuitView.as_view(), name='projects_project_quit'),
    url('^(?P<pk>\d+)/delete/$',
        ProjectDeleteView.as_view(), name='projects_project_delete'),
    url('^(?P<slug>[\w_-]+)/$', 
        ProjectDetailView.as_view(), name='projects_project_detail'),
)
