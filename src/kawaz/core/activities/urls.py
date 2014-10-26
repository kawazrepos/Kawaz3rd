__author__ = 'giginet'

from django.conf.urls import patterns, url

from .views import ActivityListView


urlpatterns = patterns('',
                       url(r'^$', ActivityListView.as_view(),
                           name='activities_activity_list'),
                       )
