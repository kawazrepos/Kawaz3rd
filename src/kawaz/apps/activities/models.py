# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import pickle
from django.db import models
from django.db.models import Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext as _


SNAPSHOT_CACHE_NAME = '_snapshot_cached'


class ActivityManager(models.Manager):
    def get_queryset(self):
        # defer '_snapshot' column which only required during signal handling
        # to accelerate database access 
        return super().get_queryset().defer('_snapshot')

    def latests(self):
        """
        Return latest activities of each particular content_objects
        """
        # find created_at list of latest activities of each particular
        # content_objects
        qs = self.get_queryset()
        qs = qs.values('content_type_id', 'object_id')
        qs = qs.annotate(created_at=Max('created_at'))
        created_ats = qs.order_by().values_list('created_at', flat=True)
        # return activities corresponding to the latests
        return self.filter(created_at__in=created_ats)


class Activity(models.Model):
    status = models.CharField(max_length=30)
    remarks = models.TextField(default='')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField('Object ID')
    content_object = GenericForeignKey()
    _snapshot = models.BinaryField(default=None, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = ActivityManager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

    def __repr__(self):
        return "<Activity: {}>".format(self.pk)

    @property
    def snapshot(self):
        if not hasattr(self, SNAPSHOT_CACHE_NAME):
            if self._snapshot:
                snapshot = pickle.loads(self._snapshot)
            else:
                snapshot = None
            setattr(self, SNAPSHOT_CACHE_NAME, snapshot)
        return getattr(self, SNAPSHOT_CACHE_NAME)

    @snapshot.setter
    def snapshot(self, value):
        if value:
            snapshot = pickle.dumps(value)
        else:
            snapshot = None
        self._snapshot = snapshot
        # delete cached object
        if hasattr(self, SNAPSHOT_CACHE_NAME):
            delattr(self, SNAPSHOT_CACHE_NAME)

    @property
    def previous(self):
        """
        Get previous activity model of a particular content_object which
        this activity target to
        """
        qs = Activity.objects.all()
        if self.pk:
            qs = qs.exclude(created_at__gte=self.created_at)
        qs = qs.filter(content_type=self.content_type,
                       object_id=self.object_id)
        return qs.order_by().last()
