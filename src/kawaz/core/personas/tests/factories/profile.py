import factory
import datetime
from django.utils import timezone
from .persona import PersonaFactory
from ...models import Profile, Skill, Service, Account


class ProfileFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Profile

    birthday = datetime.date(2009, 10, 15)
    place = 'グランエターナ'
    url = 'http://www.kawaz.org/'
    user = factory.SubFactory(PersonaFactory)


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
    url_pattern = 'http://twitter.com/{username}/'


class AccountFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Account

    service = factory.SubFactory(ServiceFactory)
    profile = factory.SubFactory(ProfileFactory)
    username = 'kawaz_tan'

