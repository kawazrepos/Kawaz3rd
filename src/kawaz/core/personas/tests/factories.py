import factory
from ..models import Persona

class PersonaFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Persona
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    last_name = 'Inonaka'
    first_name = 'Kawaz'
    username = factory.sequence(lambda n: 'kawaztan{0}'.format(n))
    email = 'webmaster@kawaz.org'
    password = 'pass'

    nickname = 'かわずたん'
    quotes = 'けろーん'
    gender = 'woman'

    role = 'children'