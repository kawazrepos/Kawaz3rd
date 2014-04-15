import types
from django.conf import settings

def validate_on_save():
    """
    class decorator to enable validation when model was saved.

    Usage :
    @validate_on_save
    class Entry(models.Model):
        def clean(self):
            if self.number < 0:
                raise ValidationError('number must be positive')
    """
    def decorated(klass):
        save = klass.save
        def wrapper(self, force_insert=False, force_update=False, **kwargs):
            if not (force_insert or force_update):
                if settings.VALIDATE_ON_SAVE:
                    self.full_clean()
            types.MethodType(save, self)(force_insert, force_update, **kwargs)
        setattr(klass, 'save', wrapper)
        return klass
    return decorated