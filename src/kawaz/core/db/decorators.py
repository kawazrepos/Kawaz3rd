from functools import wraps

def validate_on_save(klass):
    """
    A class decorator to enable auto validation on model save

    You can stop automatical validation with setting ``True`` to
    ``VALIDATE_ON_SAVE_DISABLE``

    Usage:
        >>> from django.db import models
        >>> from django.core.exceptions import ValidationError
        >>> @validation_on_save
        >>> class Entry(models.Model):
        ...     def clean(self):
        ...         raise ValidationError
    """
    # store origianl save method
    original_save = klass.save

    # ref: https://docs.djangoproject.com/en/dev/ref/models/instances/#saving-objects
    def wrapper(self, *args, **kwargs):
        from django.conf import settings    # this should be loaded in run time
        if not getattr(settings, 'VALIDATE_ON_SAVE_DISABLE', False):
            # call full_clean() method to run the validation.
            # should be called as the way below but self.full_clean() way
            klass.full_clean(self)
        # call original save method and return the value
        return original_save(self, *args, **kwargs)

    # overwrap original save method
    setattr(klass, 'save', wraps(original_save)(wrapper))
    return klass
