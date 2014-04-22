from django.conf.urls import patterns, url

from .views import ProfileListView
from .views import ProfileUpdateView
from .views import ProfileDetailView

urlpatterns = patterns('',
    url(r'^$', ProfileListView.as_view(), name='profiles_profile_list'),
    url(r'^update/$', ProfileUpdateView.as_view(), name='profiles_profile_update'),
    url(r'^(?P<slug>[^/]+)/$', ProfileDetailView.as_view(), name='profiles_profile_detail'),
)
