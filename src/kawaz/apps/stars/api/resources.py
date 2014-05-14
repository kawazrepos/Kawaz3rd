from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from ..models import Star
from .authorizations import StarAuthorization

class StarResource(ModelResource):
    class Meta:
        queryset = Star.objects.all()
        resource_name = 'star'
        list_allowed_methods = ['get',]
        detail_allowed_methods = ['post', 'delete']
        authorization = StarAuthorization()
        filtering = {
            'content_type' : ('exact',),
            'object_id' : ('exact',)
        }
