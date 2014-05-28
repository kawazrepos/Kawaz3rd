from django.db import models
from kawaz.core.personas.models import Persona
from kawaz.core.publishment.models import AbstractPublishmentModel


class PermissionsTestArticle(AbstractPublishmentModel):
    author = models.ForeignKey(Persona, related_name='permissiontest_article')
    title = models.CharField('Title', max_length=30)

    class Meta:
        app_label = 'permissions'
        permissions = (
            ('view_permissionstestarticle', 'Can view the articles'),
        )
