from django.db import models
from kawaz.core.personas.models import Persona
from ..models import AbstractPublishmentModel


class PublishmentTestArticle(AbstractPublishmentModel):
    author = models.ForeignKey(
        Persona, related_name='publishment_permissions_test_article_author')
    title = models.CharField('Title', max_length=30)

    class Meta:
        app_label = 'publishments'
        permissions = (
            ('view_publishmenttestarticle', 'Can view the articles'),
        )
