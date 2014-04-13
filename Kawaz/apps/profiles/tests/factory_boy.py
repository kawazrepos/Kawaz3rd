# -*- coding: utf-8 -*-
import factory
import datetime
from ..models import Skill, Profile

class SkillFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Skill

    label = u'プログラミング'
    order = 0

class ServiceFactory(factory.django.DjangoModelFactory):
    label = u'Twitter'
    description = u'廃人向けサービスです'
    url_pattern = u'http://www.twitter.com/%s'

class AccountFactory(factory.django.DjangoModelFactory):
    service = factory.SubFactory(ServiceFactory)
    account = 'kawaz_tan'

class ProfileFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Profile

    nickname = u'かわずたん'
    mood = u'けろーん'
    sex = 'woman'
    birthday = datetime.datetime(2009, 10, 15)
    place = u'グランエターナ'
    url = 'http://www.kawaz.org/'