# -*- coding: utf-8 -*-
import datetime

import factory
from ..models import Skill, Profile, Service, Account
from kawaz.core.auth.tests.factories import UserFactory


class SkillFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Skill
    FACTORY_DJANGO_GET_OR_CREATE = ('label',)

    label = u'プログラミング'
    description = u'闇の力です'
    order = 0

class ServiceFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Service
    FACTORY_DJANGO_GET_OR_CREATE = ('label',)

    label = 'Twitter'
    url_pattern = u'http://twitter.com/%s/'

class AccountFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Account

    service = factory.SubFactory(ServiceFactory)
    user = factory.SubFactory(UserFactory)
    username = 'kawaz_tan'

class ProfileFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Profile

    nickname = u'かわずたん'
    mood = u'けろーん'
    sex = 'woman'
    birthday = datetime.datetime(2009, 10, 15)
    place = u'グランエターナ'
    url = 'http://www.kawaz.org/'
    user = factory.SubFactory(UserFactory)