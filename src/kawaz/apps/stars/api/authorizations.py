from kawaz.core.api.authorizations import KawazAuthorization
from ..models import Star

class StarAuthorization(KawazAuthorization):
    model = Star
