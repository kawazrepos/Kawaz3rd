from django.conf.urls import patterns, url, include
from .views import (PersonaDetailView,
                    PersonaListView,
                    PersonaUpdateView,
                    PersonaAssignAdamView,
                    PersonaAssignSeeleView,
                    ProfileUpdateView,
                    ProfilePreviewView,
                    ServiceDetailView)
urlpatterns = patterns('',
    url(r'^$',
        PersonaListView.as_view(), name='personas_persona_list'),
    url(r'^my/update/$', PersonaUpdateView.as_view(),
        name='personas_persona_update'),
    url(r'^my/assign/adam/$', PersonaAssignAdamView.as_view(),
        name='personas_persona_assign_adam'),
    url(r'^my/assign/seele/$', PersonaAssignSeeleView.as_view(),
        name='personas_persona_assign_seele'),
    url(r'^my/profile/update/$',
        ProfileUpdateView.as_view(), name='personas_profile_update'),
    url(r'^my/profile/preview/$',
        ProfilePreviewView.as_view(), name='personas_profile_preview'),
    url(r'services/(?P<pk>\d+)/$',
        ServiceDetailView.as_view(), name='personas_service_detail'),
    # Note:
    #   PersonaDetailViewはユーザー名がURLに含まれるため上記のURLルールが先に
    #   適用されるために最後に指定される必要がある
    #   また、モデルレベルで'my'というユーザー名が許可されていないため上記
    #   によりアクセス出来ないユーザーが発生することはない
    url(r'^(?P<slug>[^/.+]+)/$',
        PersonaDetailView.as_view(), name='personas_persona_detail'),
)
