from registration.backends.default import DefaultRegistrationBackend
from .forms import KawazRegistrationForm



class KawazRegistrationBackend(DefaultRegistrationBackend):
    def get_registration_form_class(self):
        return KawazRegistrationForm

