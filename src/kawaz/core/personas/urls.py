from django.conf.urls import patterns, url, include
from .views import (PersonaDetailView,
                    PersonaListView,
                    PersonaUpdateView,
                    PersonaAssignAdamView,
                    PersonaAssignSeeleView,
                    ProfileUpdateView,
                    ProfilePreviewView)


inner_patterns = patterns('',
    url(r'^update/$', PersonaUpdateView.as_view(),
        name='personas_persona_update'),
    url(r'^assign/adam/$', PersonaAssignAdamView.as_view(),
        name='personas_persona_assign_adam'),
    url(r'^assign/seele/$', PersonaAssignSeeleView.as_view(),
        name='personas_persona_assign_seele'),
)

urlpatterns = patterns('',
    url(r'^$',
        PersonaListView.as_view(), name='personas_persona_list'),
    url(r'^profile/update/$',
        ProfileUpdateView.as_view(), name='personas_profile_update'),
    url(r'^profile/preview/$',
        ProfilePreviewView.as_view(), name='personas_profile_preview'),
    url(r'^(?P<slug>[^/]+)/$',
        PersonaDetailView.as_view(), name='personas_persona_detail'),
    url(r'^(?P<slug>[^/]+)/', include(inner_patterns)),
)
