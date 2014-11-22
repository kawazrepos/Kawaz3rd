import factory
from django.contrib.auth.hashers import make_password
from ...models import Persona


class PersonaFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Persona
    FACTORY_DJANGO_GET_OR_CREATE = ('username',)

    last_name = 'Inonaka'
    first_name = 'Kawaz'
    username = factory.sequence(lambda n: 'kawaztan{0}'.format(n))
    email = 'webmaster@kawaz.org'
    # using PostGenerationMethodCall is not working
    password = make_password('password')

    nickname = 'かわずたん'
    quotes = 'けろーん'
    gender = 'woman'

    role = 'children'

