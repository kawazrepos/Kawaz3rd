import datetime

import factory
from ..models import Skill, Profile, Service, Account
from kawaz.core.personas.tests.factories import PersonaFactory


class SkillFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Skill
    FACTORY_DJANGO_GET_OR_CREATE = ('label',)

    label = 'プログラミング'
    description = '闇の力です'
    order = 0

class ServiceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Service
    FACTORY_DJANGO_GET_OR_CREATE = ('label',)

    label = 'Twitter'
    url_pattern = 'http://twitter.com/%s/'

class AccountFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Account

    service = factory.SubFactory(ServiceFactory)
    user = factory.SubFactory(PersonaFactory)
    username = 'kawaz_tan'
    pub_state = 'public'

class ProfileFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Profile

    birthday = datetime.datetime(2009, 10, 15)
    place = 'グランエターナ'
    url = 'http://www.kawaz.org/'
    user = factory.SubFactory(PersonaFactory)