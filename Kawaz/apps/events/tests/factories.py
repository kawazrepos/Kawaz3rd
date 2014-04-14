# -*- coding: utf-8 -*-
import datetime
import factory
from Kawaz.apps.auth.tests.factories import UserFactory
from ..models import Event

class EventFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Event

    pub_state = 'public'
    title = u'焼肉食べまくる会'
    period_start = datetime.datetime(2014, 4, 14, 19, 0, 0)
    period_end = datetime.datetime(2014, 4, 14, 22, 0, 0)
    place = u'すすきの周辺'
    author = factory.SubFactory(UserFactory)
