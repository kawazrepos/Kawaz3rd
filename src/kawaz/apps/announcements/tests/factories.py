import factory
from kawaz.core.personas.tests.factories import PersonaFactory
from ..models import Announcement


class AnnouncementFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Announcement

    pub_state = 'public'
    title = '【悲報】データ消失のお知らせ'
    body = 'ごめんなさい'
    # Announcementの author はスタッフの必要がある
    author = factory.SubFactory(PersonaFactory, role='nerv')
