# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from functools import lru_cache
from django.core import serializers
from django.template import Context
from django.template.loader import select_template
from django.db.models.signals import (post_save,
                                      pre_delete,
                                      m2m_changed)
from django.contrib.contenttypes.models import ContentType
from .conf import settings
from .models import Activity
from .notifiers.registry import registry as notifier_registry


class ActivityMediator(object):
    """
    An ActivityMediator class which has responsivilities to controll automatic
    activity creation (with signal handling) or rendering.
    """
    default_template_extension = None
    template_extensions = None

    snapshot_fields = None
    snapshot_version = 1

    # if m2m_fields is None, get_m2m_fields return all many to many fields
    # registered in the model.
    # to prevent unwilling activity creation, default value is []
    m2m_fields = []

    notifiers = []

    @property
    def _default_template_extension(self):
        if self.default_template_extension:
            return self.default_template_extension
        else:
            return settings.ACTIVITIES_DEFAULT_TEMPLATE_EXTENSION

    @property
    def _template_extensions(self):
        if self.template_extensions:
            return self.template_extensions
        else:
            return settings.ACTIVITIES_TEMPLATE_EXTENSIONS

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
        # convert field names to actual field instance
        def _field_names_to_fields(field_names):
            for field_or_field_name in field_names:
                if isinstance(field_or_field_name, str):
                    yield self.model._meta.get_field(field_or_field_name)
                else:
                    yield field_or_field_name
        return tuple(_field_names_to_fields(self.m2m_fields))

    @lru_cache()
    def get_notifiers(self):
        """
        Return notifier instance which this mediator should send notification.
        """
        _notifiers = []
        for notifier in (self.notifiers or
                         settings.ACTIVITIES_DEFAULT_NOTIFIERS):
            if isinstance(notifier, str):
                notifier = notifier_registry.get(notifier)
            else:
                notifier = notifier_registry.get_or_register(notifier)
            _notifiers.append(notifier)
        return _notifiers

    def _pre_delete_receiver(self, sender, instance, **kwargs):
        if kwargs.get('raw', False):
            return
        ct = ContentType.objects.get_for_model(instance)
        activity = Activity(content_type=ct,
                            object_id=instance.pk,
                            status='deleted')
        # call user defined alternation code
        activity = self.alter(instance, activity, **kwargs)
        self._exec_post_processes_of_receivers(
            instance, activity, **kwargs
        )

    def _post_save_receiver(self, sender, instance, created, **kwargs):
        if kwargs.get('raw', False):
            return
        ct = ContentType.objects.get_for_model(instance)
        activity = Activity(content_type=ct,
                            object_id=instance.pk,
                            status='created' if created else 'updated')
        # call user defined alternation code
        activity = self.alter(instance, activity, **kwargs)
        self._exec_post_processes_of_receivers(
            instance, activity, **kwargs
        )

    def _m2m_changed_receiver(self, sender, instance, **kwargs):
        if kwargs.get('raw', False):
            return
        # call user defined alternation code
        # user need to create activity instance
        activity = self.alter(instance, None, **kwargs)
        self._exec_post_processes_of_receivers(
            instance, activity, **kwargs
        )

    def _exec_post_processes_of_receivers(self, instance, activity, **kwargs):
        if activity:
            # save snapshot if the activity is specified
            activity.snapshot = self.prepare_snapshot(
                instance, activity, **kwargs
            )
            # save the activity into the database
            activity.save()
            # notify
            if settings.ACTIVITIES_ENABLE_NOTIFICATION:
                for notifier in self.get_notifiers():
                    notifier.notify(activity)

    def connect(self, model):
        """
        Connect to the model. It is called in `Registry.register` method thus
        users should not call this method directly
        """
        self.model = model
        self.app_label = model._meta.app_label
        # connect post_save/pre_delete signal
        post_save.connect(self._post_save_receiver, sender=model,
                          weak=False)
        pre_delete.connect(self._pre_delete_receiver, sender=model,
                           weak=False)
        # connect m2m_changed signal of all ManyToMany fields
        for m2m in self.get_m2m_fields():
            m2m_changed.connect(self._m2m_changed_receiver,
                                sender=m2m.rel.through,
                                weak=False)

    def get_template_extension(self, typename=None):
        """
        Get template extension of a specified 'typename' determined from
        `template_extensions` attribute of this instance.
        It return `default_template_extension` of this instance if no extension
        is specified in `template_extensions`
        """
        return self._template_extensions.get(
            typename,
            self._default_template_extension,
        )

    def get_template_names(self, activity, typename=None):
        """
        Get a list of template name used to render the activity
        """
        app_label = self.app_label
        model = self.model.__name__.lower()
        status = activity.status
        ext = self.get_template_extension(typename)
        if typename:
            return (
                "activities/{}/{}_{}.{}{}".format(
                    app_label, model, status, typename, ext),
                "activities/{}/{}.{}{}".format(
                    app_label, status, typename, ext),
                "activities/{}.{}{}".format(
                    status, typename, ext),
                "activities/{}/{}_{}{}".format(
                    app_label, model, status, ext),
                "activities/{}/{}{}".format(
                    app_label, status, ext),
                "activities/{}{}".format(
                    status, ext),
            )
        else:
            return (
                "activities/{}/{}_{}{}".format(
                    app_label, model, status, ext),
                "activities/{}/{}{}".format(
                    app_label, status, ext),
                "activities/{}{}".format(
                    status, ext),
            )

    def alter(self, instance, activity, **kwargs):
        """
        Alternation code. Users can override this method to alter the activity
        creation. If None is returned, the activity creation will be canceled.

        Note:
            `activity.save()` will be called in downstream thus users should
            not save the activity manually. Just return the instance of an
            activity.

        Args:
            instance (instance): An instance of a target model
            activity (instance): An instance of an Activity model
            **kwargs (dict): keyword arguments which passed in signal handling

        Returns:
            None or activity instance. If None is returend, activity creation
            will be canceled.
        """
        return activity

    def prepare_snapshot(self, instance, activity, **kwargs):
        """
        Prepare snapshot which automatically saved to the activity instance

        Note:
            `activity.snapshot = mediator.prepare_snapshot(...)` will be called
            in downstream thus users should not specify the snapshot to the
            activity manually.
            Just return the instance of a snapshot.

        Args:
            instance (instance): An instance of a target model
            activity (instance): An instance of an Activity model
            **kwargs (dict): keyword arguments which passed in signal handling

        Returns:
            An instance which will be saved into `snapshot` field of activity
            instance. It will return `activity._content_object` in default.
        """
        return activity._content_object

    def serialize_snapshot(self, snapshot, fields=None, version=None):
        """
        Serialize a snapshot instance (a model instance) to a python dictionary
        via Django's model serializer.

        The following special fields will be inserted

        version (int):
            indicate a version of the snapshot. 'snapshot_version' value of the
            mediator will be stored. mainly for data migration
        extra_fields (dict):
            a dictionary which will be applied after deserialization. used for
            storing snapshots of related models of the snapshot.
            the default value is {}. override this method to modify this value

        Return value will be looked like:

            {
                'pk': 1,
                'model': 'personas.persona',
                'version': 1,
                'fields': {
                    'first_name': 'foo',
                    'last_name': 'bar',
                    ...
                },
                'extra_fields': {}
            }

        """
        fields = fields or self.snapshot_fields
        version = version or self.snapshot_version
        serialized_snapshot = serializers.serialize(
            'python', [snapshot], fields=fields
        )[0]
        serialized_snapshot['version'] = version
        serialized_snapshot['extra_fields'] = {}
        return serialized_snapshot

    def deserialize_snapshot(self, serialized_snapshot):
        """
        Deserialize a serialized python dictionary to a snapshot instance (a
        model instance) via Django's model serializer

        The following special fields will be inserted

        __version__ (int):
            indicate a version of the snapshot. 'snapshot_version' value of the
            mediator will be stored. mainly for data migration
        __extra_fields__ (dict):
            a dictionary which will be applied to the instance after
            deserialization. used for storing snapshots of related models of
            the snapshot.

        """
        snapshot = list(serializers.deserialize(
            'python', [serialized_snapshot]
        ))[0].object
        snapshot.__version__ = serialized_snapshot['version']
        snapshot.__extra_fields__ = serialized_snapshot['extra_fields']
        # override extra fields
        for name, value in serialized_snapshot['extra_fields'].items():
            if value:
                if isinstance(value, dict):
                    value = self.deserialize_snapshot(value)
                setattr(snapshot, name, value)
        return snapshot

    def prepare_context(self, activity, context, typename=None):
        """
        Prepare context which used in 'render' method.
        """
        context.update({
            'activity': activity,
            'object': activity.snapshot,
            'typename': typename,
        })
        return context

    def render(self, activity, context, typename=None):
        """
        Return rendered string of the specified activity
        """
        template_names = self.get_template_names(activity, typename)
        template = select_template(template_names)
        context = self.prepare_context(activity, context.new(context),
                                       typename=typename)
        return template.render(context)
