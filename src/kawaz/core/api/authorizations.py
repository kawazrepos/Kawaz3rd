from django.core.exceptions import ImproperlyConfigured
from tastypie.authorization import Authorization
from kawaz.core.permissions.utils import get_full_permission_name

class KawazAuthorization(Authorization):
    model = None

    def _get_full_permission_string(self, perm):
        if not self.model:
            raise ImproperlyConfigured(
                "No model to build Authorization. Provide a `model`.")
        return get_full_permission_name(perm, self.model)

    def _check_has_perm(self, bundle, perm, object_permission=False):
        user = bundle.request.user
        obj = None
        if object_permission:
            obj = bundle.obj
        return user.has_perm(self._get_full_permission_string(perm), obj=obj)

    def read_list(self, object_list, bundle):
        perm = self._get_full_permission_string('view')
        allowed = filter(lambda o: bundle.request.user.has_perm(perm, obj=o), object_list)
        return list(allowed)

    def read_detail(self, object_list, bundle):
        # Is the requested object owned by the user?
        return self._check_has_perm(bundle, 'view', True)

    def create_list(self, object_list, bundle):
        # Assuming they're auto-assigned to ``user``.
        return object_list

    def create_detail(self, object_list, bundle):
        return self._check_has_perm(bundle, 'add', False)

    def update_list(self, object_list, bundle):
        perm = self._get_full_permission_string('update')
        allowed = filter(lambda o: bundle.request.user.has_perm(perm, obj=o), object_list)
        return list(allowed)

    def update_detail(self, object_list, bundle):
        return self._check_has_perm(bundle, 'update', True)

    def delete_list(self, object_list, bundle):
        perm = self._get_full_permission_string('delete')
        allowed = filter(lambda o: bundle.request.user.has_perm(perm, obj=o), object_list)
        return list(allowed)

    def delete_detail(self, object_list, bundle):
        return self._check_has_perm(bundle, 'delete', True)
