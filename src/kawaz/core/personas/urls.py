from django.conf.urls import patterns, url
from kawaz.core.personas.views import (PersonaDetailView,
                                       PersonaUpdateView,
                                       PersonaAssignAdamView,
                                       PersonaAssignSeeleView)

urlpatterns = patterns('',
    url(r'^update/$', PersonaUpdateView.as_view(),
        name='personas_persona_update'),
    url(r'^assign/adam/$', PersonaAssignAdamView.as_view(),
        name='personas_persona_assign_adam'),
    url(r'^assign/seele/$', PersonaAssignSeeleView.as_view(),
        name='personas_persona_assign_seele'),
    url(r'^(?P<slug>[^/]+)/$',
        PersonaDetailView.as_view(), name='personas_persona_detail'),
)
