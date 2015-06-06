import factory
import datetime
from django.utils import timezone
from .persona import PersonaFactory
from ...models import Profile, Skill, Service, Account


class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Profile

    birthday = datetime.date(2009, 10, 15)
    place = 'グランエターナ'
    url = 'http://www.kawaz.org/'
    user = factory.SubFactory(PersonaFactory)


class SkillFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Skill
        django_get_or_create = ('label',)

    label = 'プログラミング'
    description = '闇の力です'
    order = 0


class ServiceFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Service
        django_get_or_create = ('label',)

    label = factory.Sequence(lambda n: 'Twitter{}'.format(n))
    url_pattern = 'http://twitter.com/{username}/'


class AccountFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Account

    service = factory.SubFactory(ServiceFactory)
    profile = factory.SubFactory(ProfileFactory)
    username = factory.Sequence(lambda n: 'kawaz_tan{}'.format(n))

