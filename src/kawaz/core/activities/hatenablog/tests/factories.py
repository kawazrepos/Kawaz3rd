import datetime
from django.utils import timezone
import factory
from ..models import HatenablogEntry

BASE_URL = 'http://blog.kawaz.org/20150701/vox-won-iga{}'


class HatenablogEntryFactory(factory.DjangoModelFactory):

    class Meta:
        model = HatenablogEntry
        django_get_or_create = ('url',)

    title = "VOXQUARTERがIndie Game Awardを獲得しました"
    thumbnail = "thumbnails/activities/contrib/hatenablog/filename.png"
    created_at = datetime.datetime(2015, 7, 1, tzinfo=timezone.utc)
    url = factory.Sequence(lambda n: BASE_URL.format(n))
