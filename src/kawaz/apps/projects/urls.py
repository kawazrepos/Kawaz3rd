from django.conf.urls import patterns, url

from .views import ProjectListView
from .views import ProjectUpdateView
from .views import ProjectCreateView
from .views import ProjectDeleteView
from .views import ProjectDetailView
from .views import ProjectAuthorListView
from .views import ProjectCategoryListView

urlpatterns = patterns('',
    url('^$',                               ProjectListView.as_view(),         name='projects_project_list'),
    url('^author/(?P<author>[^/]+)/$',      ProjectAuthorListView.as_view(),   name='projects_project_author_list'),
    url('^category/(?P<category>[^/]+)/$',  ProjectCategoryListView.as_view(), name='projects_project_category_list'),
    url('^create/$',                        ProjectCreateView.as_view(),       name='projects_project_create'),
    url('^(?P<object_id>\d+)/update/$',     ProjectUpdateView.as_view(),       name='projects_project_update'),
    url('^(?P<object_id>\d+)/delete/$',     ProjectDeleteView.as_view(),       name='projects_project_delete'),
    url('^(?P<slug>[\w_-]+)/$',             ProjectDetailView.as_view(),       name='projects_project_detail'),
)