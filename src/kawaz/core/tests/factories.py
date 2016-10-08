import factory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType


class PermissionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Permission

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if 'model' in kwargs and 'name' in kwargs:
            model = kwargs.pop('model')
            kwargs['content_type'] = ContentType.objects.get_for_model(model)
            model_name = model._meta.object_name.lower()
            kwargs['codename'] = '{}_{}'.format(kwargs['name'], model_name)
        return super()._create(model_class, *args, **kwargs)