import factory
from registration.models import RegistrationProfile
from kawaz.core.personas.tests.factories import PersonaFactory

class RegistrationProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = RegistrationProfile

    user = factory.SubFactory(PersonaFactory, is_active=False)
    _status = 'untreated'
    activation_key = 'this_is_an_activation_key'