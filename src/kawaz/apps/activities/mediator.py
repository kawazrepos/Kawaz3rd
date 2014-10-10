# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.template import Context
from django.template.loader import select_template
from django.db.models.signals import (post_save,
                                      pre_delete,
                                      m2m_changed)
from django.contrib.contenttypes.models import ContentType
from .models import Activity


class ActivityMediator(object):
    """
    An ActivityMediator class which has responsivilities to controll automatic
    activity creation (with signal handling) or rendering.
    """
    use_snapshot = False

    def _pre_delete_receiver(self, sender, instance, **kwargs):
        ct = ContentType.objects.get_for_model(instance)
        activity = Activity(content_type=ct,
                            object_id=instance.pk,
                            status='deleted')
        # call user defined alternation code
        activity = self.alter(instance, activity, **kwargs)
        if activity:
            # save current instance snapshot if 'use_snapshot'
            if self.use_snapshot:
                activity.snapshot = instance
            activity.save()

    def _post_save_receiver(self, sender, instance, created, **kwargs):
        ct = ContentType.objects.get_for_model(instance)
        activity = Activity(content_type=ct,
                            object_id=instance.pk,
                            status='created' if created else 'updated')
        # call user defined alternation code
        activity = self.alter(instance, activity, **kwargs)
        if activity:
            # save current instance snapshot if 'use_snapshot'
            if self.use_snapshot:
                activity.snapshot = instance
            activity.save()

    def _m2m_changed_receiver(self, sender, instance, **kwargs):
        # call user defined alternation code
        # user need to create activity instance
        activity = self.alter(instance, None, **kwargs)
        if activity:
            # save current instance snapshot if 'use_snapshot'
            if self.use_snapshot:
                activity.snapshot = instance
            activity.save()

    def connect(self, model):
        """
        Connect to the model. It is called in `Registry.register` method thus
        users should not call this method directly
        """
        self.model = model
        self.app_label = model._meta.app_label
        # connect post_save signal
        post_save.connect(self._post_save_receiver, sender=model,
                          weak=False)
        pre_delete.connect(self._pre_delete_receiver, sender=model,
                           weak=False)
        m2m_changed.connect(self._m2m_changed_receiver, sender=model,
                            weak=False)

    def get_template_names(self, activity):
        """
        Get a list of template name used to render the activity
        """
        app_label = self.app_label
        model = self.model.__name__.lower()
        status = activity.status
        return (
            "activities/{}/{}_{}.html".format(app_label, model, status),
            "activities/{}/{}.html".format(app_label, status),
            "activities/{}.html".format(status),
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

    def prepare_context(self, activity, context):
        """
        Prepare context which used in 'render' method.
        """
        context.update({
            'activity': activity,
            'object': activity.content_object
        })
        return context

    def render(self, activity, context):
        """
        Return rendered string of the specified activity
        """
        template_names = self.get_template_names(activity)
        template = select_template(template_names)
        context = self.prepare_context(activity, context.new())
        return template.render(context)
