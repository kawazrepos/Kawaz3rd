# coding=utf-8
"""
"""

import pickle
from django.db import models
from django.db.models import Max, Q
from django.core import serializers
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext as _


SNAPSHOT_CACHE_NAME = '_snapshot_cached'

class ActivityLatestsQuerySet(models.QuerySet):
    def get_base_population(self):
        """
        Return pks of the latest activities of each particular content_objects
        """
        # find created_at list of latest activities of each particular
        # content_objects
        # it use 'pk' instead of 'created_at' to filter latest while
        #   - more than two activities which has same 'created_at' is possible
        #   - newer activity have grater pk
        if not hasattr(self, '_base_population'):
            qs = self.values('content_type_id', 'object_id', 'id')
            qs = qs.annotate(pk=Max('id'))
            self._base_population = qs.values_list('pk', flat=True)
        return self._base_population

    def _fetch_all(self):
        # filter internal query with the base population
        # the base population use 'self' thus LIMIT/OFFSET will be applied
        # to the base population query as well
        self.query.add_q(Q(pk__in=self.get_base_population()))
        super()._fetch_all()

    def __getitem__(self, k):
        # OFFSET/LIMIT should only be applied into the subquery
        if isinstance(k, slice):
            qs = self._clone()
            if k.start is not None:
                start = int(k.start)
            else:
                start = None
            if k.stop is not None:
                stop = int(k.stop)
            else:
                stop = None
            qs.get_base_population().query.set_limits(start, stop)
            # Note:
            #   _fetch_all is called in __iter__
            return list(qs)[::k.step] if k.step else qs
        else:
            return super().__getitem__(k)


class ActivityManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related('content_type')
        return qs

    def latests(self):
        """
        Return latest activities of each particular content_objects
        """
        qs = super().get_queryset()
        qs = ActivityLatestsQuerySet(
            model=qs.model,
            query=qs.query,
            using=qs._db,
            hints=qs._hints,
        )
        return qs

    def get_for_model(self, model):
        """
        Get activities related to the specified model
        """
        ct = ContentType.objects.get_for_model(model)
        return self.filter(content_type=ct)

    def get_for_object(self, obj):
        """
        Get activities related to the specified object
        """
        ct = ContentType.objects.get_for_model(obj)
        return self.filter(content_type=ct, object_id=obj.pk)


class Activity(models.Model):
    """
    A model wihch represent create/update/delete (and user specified status
    changes) activity of specified models
    """
    status = models.CharField(max_length=30)
    remarks = models.TextField(default='')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField('Object ID')
    _snapshot = models.BinaryField(default=None, null=True)
    _content_object = GenericForeignKey()

    created_at = models.DateTimeField(auto_now_add=True)

    objects = ActivityManager()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')

    def __repr__(self):
        return "<Activity: {}:{}:{}>".format(self.content_type.model,
                                             self.object_id,
                                             self.status)

    @property
    def mediator(self):
        from .registry import registry
        return registry.get(self)

    @property
    def snapshot(self):
        """
        Get a pickled object from database
        """
        if not hasattr(self, SNAPSHOT_CACHE_NAME):
            snapshot = None
            if self._snapshot:
                serialized_obj = pickle.loads(self._snapshot)
                if serialized_obj and isinstance(serialized_obj, dict):
                    snapshot = self.mediator.deserialize_snapshot(
                        serialized_obj
                    )
                else:
                    snapshot = serialized_obj
            setattr(self, SNAPSHOT_CACHE_NAME, snapshot)
        return getattr(self, SNAPSHOT_CACHE_NAME)

    @snapshot.setter
    def snapshot(self, value):
        """
        Set object to database as pickled object
        """
        if value:
            serialized_obj = self.mediator.serialize_snapshot(value)
            snapshot = pickle.dumps(serialized_obj)
        else:
            snapshot = None
        self._snapshot = snapshot
        # delete cached object
        if hasattr(self, SNAPSHOT_CACHE_NAME):
            delattr(self, SNAPSHOT_CACHE_NAME)

    @property
    def previous(self):
        """
        Get a previous activity instance which have same content_type and
        object_id as this activity instance.
        This is a shortcut property of the following code

            qs = activity.get_previous_activities()
            previous = qs.first()

        """
        qs = self.get_previous_activities()
        return qs.first()

    def get_related_activities(self):
        """
        Get a queryset of activities which have same content_type and object_id
        as this activity instance except the activity itself.
        Note that the queryset is cached in the instance thus you may need to
        re-get the instance from a database to update the cache.
        """
        cache_name = '_related_cache'
        if not hasattr(self, cache_name):
            qs = Activity.objects.filter(content_type=self.content_type,
                                         object_id=self.object_id)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            setattr(self, cache_name, qs)
        return getattr(self, cache_name)

    def get_previous_activities(self):
        """
        Get a queryset of activities which is smilar to the queryset returned
        by `get_related_activities` method but only older activities are
        contained.
        """
        qs = self.get_related_activities()
        if self.pk:
            qs = qs.exclude(created_at__gte=self.created_at)
        return qs

    def get_next_activities(self):
        """
        Get a queryset of activities which is smilar to the queryset returned
        by `get_related_activities` method but only newer activities are
        contained.
        """
        qs = self.get_related_activities()
        if self.pk:
            qs = qs.exclude(created_at__lte=self.created_at)
        return qs
