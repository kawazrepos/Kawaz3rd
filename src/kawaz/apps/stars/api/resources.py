from tastypie.resources import ModelResource
from tastypie import fields
from ..models import Star
from .authorizations import StarAuthorization

class StarResource(ModelResource):

    content_type = fields.IntegerField(attribute='content_type_id')

    class Meta:
        queryset = Star.objects.all()
        resource_name = 'star'
        list_allowed_methods = ['get','post']
        detail_allowed_methods = ['delete',]
        authorization = StarAuthorization()
        filtering = {
            'content_type' : ('exact',),
            'object_id' : ('exact',)
        }

    def hydrate(self, bundle):
        # set author automatically
        if bundle.obj.pk is None:
            # This method seems to be called before checking authorization by StarAuthorization
            # request.user may be AnonymousUser
            # So, I checked authentication status of the user.
            if bundle.request.user.is_authenticated():
                bundle.obj.author = bundle.request.user
        return bundle
