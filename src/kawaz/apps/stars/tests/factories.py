import factory
from ..models import Star
from kawaz.core.personas.tests.factories import PersonaFactory
from kawaz.apps.blogs.tests.factories import EntryFactory

class StarFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Star

    author = factory.SubFactory(PersonaFactory)
    content_object = factory.SubFactory(EntryFactory)
    comment = 'コメント'
    tag = 'tag'
