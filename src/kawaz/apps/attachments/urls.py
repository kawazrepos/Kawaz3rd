from django.conf.urls import patterns, url
from .views import MaterialDetailView


urlpatterns = patterns('',
    url(r'^(?P<slug>[^/]+)/$',
        MaterialDetailView.as_view(),
        name='attachments_material_detail'),
)
