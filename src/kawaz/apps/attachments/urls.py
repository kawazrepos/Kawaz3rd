from django.conf.urls import patterns, url
from rest_framework import routers

from .views import MaterialDetailView
from .api.views import MaterialViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'materials', MaterialViewSet, base_name='material')

urlpatterns = patterns('',
    url(r'^(?P<slug>[^/]+)/$', MaterialDetailView.as_view(), name='attachments_material_detail'),
) + router.urls