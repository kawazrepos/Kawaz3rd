from django.db import models
from kawaz.core.publishments.models import PUB_STATES
from ..models import Persona


class PersonaTestArticle(models.Model):
    pub_state = models.CharField("Publish status",
                                 max_length=10, choices=PUB_STATES,
                                 default="public")
    title = models.CharField('Title', max_length=30)
    author = models.ForeignKey(
        Persona, related_name='personatest_article_author')

    class Meta:
        app_label = 'personas'
        permissions = (
            ('view_personatestarticle', 'Can view the articles'),
        )
