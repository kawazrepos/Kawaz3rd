import factory
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Announcement

class AnnouncementFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Announcement

    pub_state = 'public'
    title = '【悲報】データ消失のお知らせ'
    body = 'ごめんなさい'
    silently = False
    author = factory.SubFactory(PersonaFactory)