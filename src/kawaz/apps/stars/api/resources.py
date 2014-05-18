from tastypie import fields
from tastypie.authentication import SessionAuthentication
from kawaz.core.api.resources import KawazModelResource
from kawaz.core.api.authorizations import PermissionBasedAuthorization
from ..models import Star

class StarResource(KawazModelResource):
    author_field_name = 'author'
    content_type = fields.IntegerField(attribute='content_type_id')

    class Meta:
        resource_name = 'star'
        queryset = Star.objects.all()
        list_allowed_methods = ['get','post']
        detail_allowed_methods = ['delete',]
        always_return_data = True
        authorization = PermissionBasedAuthorization()
        authentication = SessionAuthentication()
        filtering = {
            'content_type' : ('exact',),
            'object_id' : ('exact',)
        }
