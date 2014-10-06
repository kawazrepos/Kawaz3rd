from django.conf.urls import patterns, include, url
from django.conf import settings


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^central-dogma/', include(admin.site.urls)),
    url(r'^api/', include('kawaz.api.urls')),
    url(r'^announcements/', include('kawaz.apps.announcements.urls')),
    url(r'^events/', include('kawaz.apps.events.urls')),
    url(r'^members/', include('kawaz.apps.profiles.urls')),
    url(r'^blogs/', include('kawaz.apps.blogs.urls')),
    url(r'^products/', include('kawaz.apps.products.urls')),
    url(r'^projects/', include('kawaz.apps.projects.urls')),
    url(r'^attachments/', include('kawaz.apps.attachments.urls')),
    url(r'^registration/', include('kawaz.core.personas.urls')),
    url(r'^registration/', include('registration.urls')),
)

from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
