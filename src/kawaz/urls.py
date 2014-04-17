from django.conf.urls import patterns, include, url
from django.contrib import admin

from kawaz.core.views import IndexView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^events/', include('kawaz.apps.events.urls')),
    url(r'^$', IndexView.as_view(), name='kawaz_index')
)
