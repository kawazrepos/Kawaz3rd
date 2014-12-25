# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from functools import lru_cache, wraps
from django.db.models import ObjectDoesNotExist
from django.db.models.signals import (pre_save,
                                      post_save,
                                      pre_delete,
                                      m2m_changed)
from django.contrib.contenttypes.models import ContentType
from models import Wall, History
from investigator import Investigator


def ignore_batch_processed(fn):
    """
    Ignore batch processed signals
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        if kwargs.get('row', False):
            # do nothing while it is processed by batch process
            return
        return fn(*args, **kwargs)
    return inner


class Mediator(object):
    include_fields = None
    exclude_fields = None
    m2m_fields = None

    def get_include_fields(self):
        return self.include_fields

    def get_exclude_fields(self):
        return self.exclude_fields

    @lru_cache()
    def get_m2m_fields(self):
        """
        Return m2m fields which will be watched for recognizing m2m changes

        It simply return a list defined as `m2m_fields` attribute or all
        many to many fields defined in the connected model if `m2m_fields`
        is `None`.
        """
        if self.m2m_fields is None:
            return tuple(self.model._meta.local_many_to_many)

        def _field_names_to_fields(field_names):
            for field_or_field_name in field_names:
                if isinstance(field_or_field_name, str):
                    yield self.model._meta.get_field(field_or_field_name)
                else:
                    yield field_or_field_name
        return tuple(_field_names_to_fields(self.m2m_fields))

    def connect(self, model):
        """
        Connect this mediator to a model.

        This method will be called in ``Registry.register`` method and users
        don't need to call it manually.
        """
        self.model = model
        self.app_label = model._meta.app_label
        self.investigator = Investigator(self.model,
                                         self.get_include_fields(),
                                         self.get_exclude_fields())
        # connect pre_save/post_save
        pre_save.connect(self._pre_save_receiver, sender=model,
                         weak=False)
        post_save.connect(self._post_save_receiver, sender=model,
                          weak=False)
        pre_delete.connect(self._pre_delete_receiver, sender=model,
                           weak=False)
        # connect m2m_changed signal of all ManyToMany fields
        for m2m in self.get_m2m_fields():
            m2m_changed.connect(self._m2m_changed_receiver,
                                sender=m2m.rel.through,
                                weak=False)

    @ignore_batch_processed
    def _pre_save_receiver(self, sender, instance, **kwargs):
        self.investigator.prepare(instance)

    @ignore_batch_processed
    def _post_save_receiver(self, sender, instance, created, **kwargs):
        wall = self.alter_wall(Wall(content_object=instance), instance)
        wall.save()
        histories = []
        if not created:
            for field, old, new in self.investigator.investigate(instance):
                if not old:
                    status = 'created'
                elif not new:
                    status = 'deleted'
                else:
                    status = 'updated'
                histories.append(History(
                    wall=wall,
                    status=status,
                    extra={
                        'field': field,
                        'old': old,
                        'new': new,
                    },
                ))
        histories = self.alter_histories(histories, wall, instance)
        for history in histories:
            history.save()

    @ignore_batch_processed
    def _pre_delete_receiver(self, sender, instance, **kwargs):
        try:
            wall = Wall.objects.get(content_object=instance)
        except ObjectDoesNotExist:
            return
        wall = self.alter_wall(wall, instance)
        wall.is_deleted = True
        wall.save()

    @ignore_batch_processed
    def _m2m_changed_receiver(self, sender, instance,
                              action, reverse, model,
                              pk_set, **kwargs):
        if reverse or action in ('pre_add', 'pre_remove'):
            # reverse m2m signal should not be treated
            return

        # find field name of sender
        def _find_field_name(sender):
            for field in self.get_m2m_fields():
                if field.through == sender:
                    return field.name
                return None
        field_name = _find_field_name(sender)
        if field_name is None:
            return

        if action == 'pre_clean':
            # pre_clean/post_clean does not have 'pk_set' thus get current
            # pk_set from the instance and cache
            self._pk_set_cached = [x.pk for x in getattr(instance, field_name)]
            return
        pk_set = pk_set or getattr(self, '_pk_set_cached', [])

        wall = self.alter_wall(Wall(content_object=instance), instance)
        wall.save()
        histories = []
        for related in model._default_manager.filter(pk__in=pk_set):
            ct = ContentType.objects.get_for_model(related)
            natural_key = ct.natural_key()
            if action == 'post_add':
                status = 'created'
                old = None
                new = related.pk
            elif action in ('post_remove', 'post_clean'):
                status = 'deleted'
                old = related.pk
                new = None
            histories.append(History(
                wall=wall,
                status=status,
                extra={
                    'model': natural_key,
                    'old': old,
                    'new': new,
                }
            ))
        histories = self.alter_histories(histories, wall, instance)
        for history in histories:
            history.save()

    def alter_wall(self, wall, instance):
        return wall

    def alter_histories(self, histories, wall, instance):
        return histories
