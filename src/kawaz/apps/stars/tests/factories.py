import factory
from ..models import Star
from kawaz.core.personas.tests.factories import PersonaFactory

class StarFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Star

    author = factory.SubFactory(PersonaFactory)
    content_object = factory.SubFactory(PersonaFactory)
    comment = 'コメント'
    tag = 'tag'
