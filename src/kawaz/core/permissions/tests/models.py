from django.db import models
from kawaz.core.permissions import PUB_STATES
from kawaz.core.personas.models import Persona

class Article(models.Model):
    title = models.CharField('Title', max_length=30)
    written_by = models.ForeignKey(Persona)
    publish_status = models.CharField('Publish State', choices=PUB_STATES, max_length=10, default='public')

    class Meta:
        app_label = 'permissions'
        permissions = (
            ('view_article', 'Can view the articles'),
        )
