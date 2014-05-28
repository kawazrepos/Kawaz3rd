from kawaz.core.api.authorizations import PermissionBasedAuthorization

class MaterialAuthorization(PermissionBasedAuthorization):
    def read_list(self, object_list, bundle):
        # 全てのオブジェクトが読める
        return object_list

    def read_detail(self, object_list, bundle):
        # 全てのオブジェクトが読める
        return True