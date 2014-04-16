import factory
from ..models import Category, Entry
from kawaz.core.personas.tests.factories import PersonaFactory

class CategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Category

    label = 'イベントレポート'
    author = factory.SubFactory(PersonaFactory)

class EntryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Entry

    pub_state = 'public'
    title = '焼肉食べまくる会に参加してきました'
    body = 'カルビがおいしかった（小並感）'
    author = factory.SubFactory(PersonaFactory)
