from django.conf.urls import patterns, include, url
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings


from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^login/$', auth_views.login,
        name='login', kwargs=dict(
            template_name='login.html'
        )),
    url(r'^logout/$', auth_views.logout, 
        name='logout', kwargs=dict(
            template_name='logout.html',
            next_page='/',
        )),
    url(r'^central-dogma/', include(admin.site.urls)),
    url(r'^central-dogma/doc/', include('django.contrib.admindocs.urls')),
    url(r'^api/', include('kawaz.api.urls')),
    url(r'^activities/', include('kawaz.core.activities.urls')),
    url(r'^announcements/', include('kawaz.apps.announcements.urls')),
    url(r'^events/', include('kawaz.apps.events.urls')),
    url(r'^blogs/', include('kawaz.apps.blogs.urls')),
    url(r'^products/', include('kawaz.apps.products.urls')),
    url(r'^projects/', include('kawaz.apps.projects.urls')),
    url(r'^attachments/', include('kawaz.apps.attachments.urls')),
    url(r'^members/', include('kawaz.core.personas.urls')),
    url(r'^registration/', include('kawaz.core.registrations.urls')),
    url(r'^comments/', include('django_comments.urls')),
)

if not settings.PRODUCT:
    # 本番環境以外では開発用サーバーにて静的ファイルも提供
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += (
        url(r'^favicon\.ico$',
            RedirectView.as_view(url='/statics/favicon.ico')),
    )
