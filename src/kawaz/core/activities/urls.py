from django.conf.urls import url

from .views import ActivityListView


urlpatterns = [
    url(r'^$', ActivityListView.as_view(),
        name='activities_activity_list'),
]
