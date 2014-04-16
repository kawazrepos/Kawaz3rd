import datetime

import factory
from kawaz.core.persona.tests.factories import UserFactory
from ..models import Event


class EventFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Event

    pub_state = 'public'
    title = '焼肉食べまくる会'
    period_start = factory.LazyAttribute(lambda o: datetime.datetime.now() + datetime.timedelta(hours=1))
    period_end = factory.LazyAttribute(lambda o: datetime.datetime.now() + datetime.timedelta(hours=4))
    place = 'すすきの周辺'
    organizer = factory.SubFactory(UserFactory)
