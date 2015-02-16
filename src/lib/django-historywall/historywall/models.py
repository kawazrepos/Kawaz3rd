# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models
from django.db.models import Max
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext as _
from jsonfield import JSONField


class Wall(models.Model):
    """
    A model which represent a history wall of a particular object
    """
    content_type = models.ForeignKey(ContentType, editable=False)
    object_id = models.PositiveIntegerField('Object ID', editable=False)
    content_object = GenericForeignKey()
    is_deleted = models.BooleanField(_('Is deleted'), default=False)
    _index = models.PositiveIntegerField(
        _('Index'), db_column='index', db_index=True, default=0,
        help_text=_(
            "An index of appearant ordering of walls. "
            "This value will automatically be updated when new "
            "history instance of the wall is created."
        )
    )

    class Meta:
        ordering = ('_index',)
        index_together = (
            ('content_type', 'object_id'),
        )
        unique_together = (
            ('content_type', 'object_id'),
        )
        verbose_name = _('Wall')
        verbose_name_plural = _('Walls')

    @classmethod
    def _get_max_index(cls):
        return Wall.objects.aggregate(Max('_index'))['_index__max'] or 0

    @classmethod
    def _get_max_index_cache(cls):
        cache_name = '_max_index_cached'
        if not hasattr(cls, cache_name):
            cls._set_max_index_cache(cls._get_max_index())
        return getattr(cls, cache_name)

    @classmethod
    def _set_max_index_cache(cls, index):
        cache_name = '_max_index_cached'
        setattr(cls, cache_name, index)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', None)
        if update_fields is None or '_index' in update_fields:
            # automatically increase maximum value + 1 of index
            m = self.__class__._get_max_index_cache()
            if self.pk is None or self._index < m:
                self._index = m + 1
                # save max index in cache to accelerate code
                self.__class__._set_max_index_cache(self._index)
            elif self._index == m and update_fields:
                # index is not required to be updated
                kwargs['update_fields'].remove('_index')
        super().save(*args, **kwargs)


class History(models.Model):
    """
    A model which represent each create/update/delete history of a wall
    """
    wall = models.ForeignKey(
        Wall, db_index=True, editable=False, related_name='histories',
        help_text=_(
            "A wall of this history belongs."
        )
    )
    status = models.SlugField(
        _('Status'), max_length=30,
        help_text=_(
            "A status of this history. "
            "User should give a short summury of the history example "
            "'created' or 'updated'. "
            "This value will also be used to determined a template file to "
            "render."
        )
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    extra = JSONField(
        _('Extra informations'),
        default=None, null=True,
        help_text=_(
            "Extra informations of this history in JSON format. "
            "User is allowed to save any informations in this field to "
            "use in template for rendering extra informations, such as "
            "'<James> change <publishment status> from <draft> to <publish>' "
            "or so on. "
            "In this case, user need to save <who>, <field>, <from>, and <to> "
            "extra informations."
        )
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = _('History')
        verbose_name_plural = _('Histories')

    def save(self, *args, **kwargs):
        if self.pk is None:
            # automatically increase the index of the wall
            # when this history is just created
            self.wall.save(update_fields=['_index'])
        super().save(*args, **kwargs)
