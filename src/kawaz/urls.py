from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from kawaz.core.views import IndexView
from kawaz.core.api import v1_api

admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf import settings
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^announcements/', include('kawaz.apps.announcements.urls')),
    url(r'^events/', include('kawaz.apps.events.urls')),
    url(r'^members/', include('kawaz.apps.profiles.urls')),
    url(r'^blogs/', include('kawaz.apps.blogs.urls')),
    url(r'^products/', include('kawaz.apps.products.urls')),
    url(r'^projects/', include('kawaz.apps.projects.urls')),
    url(r'^stars/', include('kawaz.apps.stars.urls')),
    url(r'^$', IndexView.as_view(), name='kawaz_index'),
    url(r'^api/', include(v1_api.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
