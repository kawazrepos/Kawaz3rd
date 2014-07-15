#
# The source code in this files were forked from django-observer
# Thus the LICENSE of the codes follow MIT license
#
from django.db import models


def alias(name):
    """Define alias name of the class"""
    def decorator(cls):
        globals()[name] = cls
        return cls
    return decorator


@alias('Article')
class SingleObjectPreviewMixinTestArticle(models.Model):
    foo = models.CharField(max_length=50)
    bar = models.TextField()

