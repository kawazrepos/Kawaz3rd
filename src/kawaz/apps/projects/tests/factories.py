# -*- coding: utf-8 -*-
import factory
from kawaz.core.persona.tests.factories import UserFactory
from ..models import Category, Project

class CategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Category

    label = 'RPG'
    parent = None

class ProjectFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Project
    FACTORY_DJANGO_GET_OR_CREATE = ('slug',)

    pub_state = 'public'
    status = 'active'
    title = u'ぼくのかんがえた最強のRPG'
    slug = 'my-fantastic-rpg'

    category = factory.SubFactory(CategoryFactory)
    administrator = factory.SubFactory(UserFactory)
