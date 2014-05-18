import factory
from ..models import Star
from .models import StarTestArticle
from kawaz.core.personas.tests.factories import PersonaFactory


class ArticleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = StarTestArticle

    pub_state = 'public'
    author = factory.SubFactory(PersonaFactory)
    title = "タイトル"


class StarFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Star

    author = factory.SubFactory(PersonaFactory)
    content_object = factory.SubFactory(ArticleFactory)
    quote = "引用"

