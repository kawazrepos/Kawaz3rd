from django.conf.urls import patterns, url
from rest_framework import routers
from .api.views import StarViewSet
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'stars', StarViewSet, base_name='star')

urlpatterns =  router.urls
