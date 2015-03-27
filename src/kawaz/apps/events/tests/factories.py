import datetime
from django.utils import timezone

import factory
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Event
from ..models import Category

class CategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = Category

    label = 'ゲームオフ'
    order = 1


class EventFactory(factory.DjangoModelFactory):

    class Meta:
        model = Event

    pub_state = 'public'
    title = '焼肉食べまくる会'
    body = "カルビ食べたい"
    period_start = factory.LazyAttribute(
        lambda o: timezone.now() + datetime.timedelta(hours=1))
    period_end = factory.LazyAttribute(
        lambda o: timezone.now() + datetime.timedelta(hours=4))
    place = 'すすきの周辺'
    organizer = factory.SubFactory(PersonaFactory)
