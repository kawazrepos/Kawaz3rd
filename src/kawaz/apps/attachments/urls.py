from django.conf.urls import patterns, url

from kawaz.core.api import v1_api
from .api.resources import MaterialResource
from .views import MaterialDetailView

v1_api.register(MaterialResource())

urlpatterns = patterns('',
    url(r'^(?P<slug>[^/]+)/$', MaterialDetailView.as_view(), name='materials_material_detail'),
)