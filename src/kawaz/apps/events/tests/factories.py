import datetime

import factory
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Event
from ..models import Category

class CategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Category

    label = 'ゲームオフ'
    order = 1


class EventFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Event

    pub_state = 'public'
    title = '焼肉食べまくる会'
    period_start = factory.LazyAttribute(lambda o: datetime.datetime.now() + datetime.timedelta(hours=1))
    period_end = factory.LazyAttribute(lambda o: datetime.datetime.now() + datetime.timedelta(hours=4))
    place = 'すすきの周辺'
    organizer = factory.SubFactory(PersonaFactory)
