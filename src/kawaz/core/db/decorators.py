from functools import wraps
from django.conf import settings


# デフォルトの値を設定
setattr(settings, 'VALIDATE_ON_SAVE_DISABLE',
        getattr(settings, 'VALIDATE_ON_SAVE_DISABLE', False))


def validate_on_save(klass):
    """
    モデル保存時にバリデーションを走らせるためのクラスデコレータ

    このデコレータが指定されたモデルを保存した場合、自動的に ``full_clean()``
    が呼び出されバリデーションが走る

    Usage:
        >>> from django.db import models
        >>> from django.core.exceptions import ValidationError
        >>> @validation_on_save
        >>> class Entry(models.Model):
        ...     def clean(self):
        ...         raise ValidationError
    """
    original_save = klass.save

    def wrapper(self, *args, **kwargs):
        if not settings.VALIDATE_ON_SAVE_DISABLE:
            klass.full_clean(self)
        return original_save(self, *args, **kwargs)
    setattr(klass, 'save', wraps(original_save)(wrapper))
    return klass
