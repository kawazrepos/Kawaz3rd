from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views
from registration.urls import urlpatterns


urlpatterns += patterns('',
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'},
        name='login'),
    url(r'^logout/$', auth_views.logout,
        {'template_name': 'logout.html',
         'next_page': '/'},
        name='logout'),
    url(r'^password_change/$', auth_views.password_change,
        name='password_change'),
    url(r'^password_change/done/$', auth_views.password_change_done,
        name='password_change_done'),
    url(r'^password_reset/$', auth_views.password_reset,
        name='password_reset', kwargs=dict(
            post_reset_redirect='password_reset_done')),
    url(r'^password_reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^password_reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),
)
