from django.conf.urls import patterns, include, url
from django.contrib import admin

from kawaz.core.views import IndexView
from kawaz.core.api.urls import v1_api
from kawaz.apps.stars.api.resources import StarResource

v1_api.register(StarResource())

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^announcements/', include('kawaz.apps.announcements.urls')),
    url(r'^events/', include('kawaz.apps.events.urls')),
    url(r'^members/', include('kawaz.apps.profiles.urls')),
    url(r'^blogs/', include('kawaz.apps.blogs.urls')),
    url(r'^projects/', include('kawaz.apps.projects.urls')),
    url(r'^stars/', include('kawaz.apps.stars.urls')),
    url(r'^$', IndexView.as_view(), name='kawaz_index')
)
