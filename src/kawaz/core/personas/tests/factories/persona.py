import factory
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from ...models import Persona


class PersonaFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Persona
        django_get_or_create = ('username',)

    last_name = 'Inonaka'
    first_name = 'Kawaz'
    username = factory.sequence(lambda n: 'kawaztan{0}'.format(n))
    email = 'webmaster@kawaz.org'
    # using PostGenerationMethodCall is not working
    password = make_password('password')
    last_login = timezone.now()

    nickname = 'かわずたん'
    quotes = 'けろーん'
    gender = 'woman'

    role = 'children'

