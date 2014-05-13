# -*- coding: utf-8 -*-
import factory
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Category, Project

class CategoryFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Category
    FACTORY_DJANGO_GET_OR_CREATE = ('label',)

    label = 'RPG'
    parent = None

class ProjectFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Project
    FACTORY_DJANGO_GET_OR_CREATE = ('slug',)

    pub_state = 'public'
    status = 'active'
    title = factory.Sequence(lambda n: 'ぼくのかんがえた最強のRPG{}'.format(n))
    slug = factory.Sequence(lambda n: 'my-fantastic-rpg{}'.format(n))

    category = factory.SubFactory(CategoryFactory)
    administrator = factory.SubFactory(PersonaFactory)
