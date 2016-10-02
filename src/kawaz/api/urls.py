from django.conf.urls import url, patterns, include
from rest_framework import routers
from kawaz.apps.stars.api.views import StarViewSet
from kawaz.apps.blogs.api.views import CategoryViewSet
from kawaz.apps.attachments.api.views import MaterialViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'stars', StarViewSet)
router.register(r'materials', MaterialViewSet)
router.register(r'blogs', CategoryViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework'))
]
