from tastypie import fields
from tastypie.authentication import SessionAuthentication
from kawaz.core.api.resources import KawazModelResource
from kawaz.core.api.authorizations import PermissionBasedAuthorization
from ..models import Material

class MaterialResource(KawazModelResource):
    author_field_name = 'author'
    content_file = fields.FileField(attribute='content_file')

    class Meta:
        resource_name = 'attachments/material'
        queryset = Material.objects.all()
        list_allowed_methods = ['post',]
        detail_allowed_methods = ['put', 'delete',]
        always_return_data = True
        authorization = PermissionBasedAuthorization()
        authentication = SessionAuthentication()

    def hydrate_ip_address(self, bundle):
        try:
            # IPアドレスが取得できたら格納する
            bundle.data['ip_address'] = bundle.request.META['REMOTE_ADDR']
        except:
            # 取得に失敗したら0.0.0.0を格納する
            bundle.data['ip_address'] = '0.0.0.0'
        return bundle
