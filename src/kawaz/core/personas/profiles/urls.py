from django.conf.urls import patterns, url

from .views import ProfileUpdateView
from .views import ProfilePreview

urlpatterns = patterns('',
    url(r'^preview/$', ProfilePreview.as_view(), name='profiles_profile_preview'),
    url(r'^update/$', ProfileUpdateView.as_view(), name='profiles_profile_update'),
)
