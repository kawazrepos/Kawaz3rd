from django.db import models
from kawaz.core.personas.models import Persona
from kawaz.core.publishments.models import PUB_STATES


class PersonaTestArticle(models.Model):
    pub_state = models.CharField("Publish status",
                                 max_length=10, choices=PUB_STATES,
                                 default="public")
    author = models.ForeignKey(
        Persona, related_name='personatest_article_author')
    title = models.CharField('Title', max_length=30)

    class Meta:
        app_label = 'personas'
        permissions = (
            ('view_personatestarticle', 'Can view the articles'),
        )
