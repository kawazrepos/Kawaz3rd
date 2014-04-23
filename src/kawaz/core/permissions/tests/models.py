from django.db import models
from kawaz.core.personas.models import Persona
from kawaz.core.permissions.logics import PUB_STATES


class Article(models.Model):
    pub_state = models.CharField('Publish State', choices=PUB_STATES,
                                 max_length=10, default='public')
    author = models.ForeignKey(Persona)
    title = models.CharField('Title', max_length=30)

    class Meta:
        app_label = 'permissions'
        permissions = (
            ('view_article', 'Can view the articles'),
        )
