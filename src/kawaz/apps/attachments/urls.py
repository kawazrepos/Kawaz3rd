from django.conf.urls import url
from .views import MaterialDetailView


urlpatterns = [
    url(r'^(?P<slug>[^/]+)/$',
        MaterialDetailView.as_view(),
        name='attachments_material_detail'),
]
