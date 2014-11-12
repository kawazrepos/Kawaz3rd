# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from functools import lru_cache
from django.template import Context
from django.template.loader import select_template
from django.db.models.signals import (post_save,
                                      pre_delete,
                                      m2m_changed)
from django.contrib.contenttypes.models import ContentType
from .conf import settings
from .models import Activity


class ActivityMediator(object):
    """
    An ActivityMediator class which has responsivilities to controll automatic
    activity creation (with signal handling) or rendering.
    """
    default_template_extension = None
    template_extensions = None

    # if m2m_fields is None, get_m2m_fields return all many to many fields
    # registered in the model.
    # to prevent unwilling activity creation, default value is []
    m2m_fields = []

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

    def _pre_delete_receiver(self, sender, instance, **kwargs):
        ct = ContentType.objects.get_for_model(instance)
        activity = Activity(content_type=ct,
                            object_id=instance.pk,
                            status='deleted')
        # call user defined alternation code
        activity = self.alter(instance, activity, **kwargs)
        if activity:
            # save current instance as a snapshot
            # the target instance might be changed thus use _content_object
            # instead of 'instance'
            activity.snapshot = self.prepare_snapshot(instance,
                                                      activity, **kwargs)
            activity.save()

    def _post_save_receiver(self, sender, instance, created, **kwargs):
        ct = ContentType.objects.get_for_model(instance)
        activity = Activity(content_type=ct,
                            object_id=instance.pk,
                            status='created' if created else 'updated')
        # call user defined alternation code
        activity = self.alter(instance, activity, **kwargs)
        if activity:
            # save current instance as a snapshot
            # the target instance might be changed thus use _content_object
            # instead of 'instance'
            activity.snapshot = self.prepare_snapshot(instance,
                                                      activity, **kwargs)
            activity.save()

    def _m2m_changed_receiver(self, sender, instance, **kwargs):
        # call user defined alternation code
        # user need to create activity instance
        activity = self.alter(instance, None, **kwargs)
        if activity:
            # save current instance as a snapshot
            # the target instance might be changed thus use _content_object
            # instead of 'instance'
            activity.snapshot = self.prepare_snapshot(instance,
                                                      activity, **kwargs)
            activity.save()

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
        context = self.prepare_context(activity, context.new(),
                                       typename=typename)
        return template.render(context)
