import datetime
import factory
from ..models import RecentActivity


class RecentActivityFactory(factory.DjangoModelFactory):
    FACTORY_FOR = RecentActivity
    FACTORY_DJANGO_GET_OR_CREATE = ('url',)

    title = "VOXQUARTERがIndie Game Awardを獲得しました"
    thumbnail = "thumbnails/recent_activities/filename.png"
    publish_at = datetime.datetime(2015, 7, 1)
    url = factory.Sequence(lambda n: "http://blog.kawaz.org/20150701/vox-won-iga{}".format(n))
