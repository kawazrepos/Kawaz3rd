# -*- coding: utf-8 -*-
import factory
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Category, Project

class CategoryFactory(factory.DjangoModelFactory):

    class Meta:
        model = Category
        django_get_or_create = ('label',)

    label = 'RPG'

class ProjectFactory(factory.DjangoModelFactory):

    class Meta:
        model = Project
        django_get_or_create = ('slug',)

    pub_state = 'public'
    status = 'active'
    title = factory.Sequence(lambda n: 'ぼくのかんがえた最強のRPG{}'.format(n))
    slug = factory.Sequence(lambda n: 'my-fantastic-rpg{}'.format(n))

    category = factory.SubFactory(CategoryFactory)
    administrator = factory.SubFactory(PersonaFactory)
