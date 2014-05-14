from kawaz.core.api.authorizations import KawazAuthorization
from ..models import Star

class StarAuthorization(KawazAuthorization):
    model = Star

    def read_list(self, object_list, bundle):
        # all user can view all stars
        return object_list

    def read_detail(self, object_list, bundle):
        # all user can view all stars
        return True