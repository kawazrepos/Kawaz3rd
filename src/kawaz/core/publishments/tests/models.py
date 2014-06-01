from django.db import models
from kawaz.core.personas.models import Persona
from ..models import PUB_STATES


class PublishmentTestArticle(models.Model):
    pub_state = models.CharField("Publish status",
                                 max_length=10, choices=PUB_STATES,
                                 default="public")
    author = models.ForeignKey(
        Persona, related_name='publishment_permissions_test_article_author')
    title = models.CharField('Title', max_length=30)

    class Meta:
        app_label = 'publishments'
        permissions = (
            ('view_publishmenttestarticle', 'Can view the articles'),
        )
