from django.conf.urls import patterns, url

from kawaz.core.api import v1_api
from .api.resources import StarResource

v1_api.register(StarResource())

urlpatterns = patterns('',
)