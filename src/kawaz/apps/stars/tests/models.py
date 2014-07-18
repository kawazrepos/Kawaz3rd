# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models
from kawaz.core.personas.models import Persona
from kawaz.core.publishments.models import PUB_STATES


class StarTestArticle(models.Model):
    pub_state = models.CharField("Publish status",
                                 max_length=10, choices=PUB_STATES,
                                 default="public")
    author = models.ForeignKey(Persona)
    title = models.CharField('Title', max_length=30)

    class Meta:
        app_label = 'stars'
        permissions = (
            ('view_startestarticle', 'Can view the articles'),
        )


from permission import add_permission_logic
from kawaz.core.personas.perms import KawazAuthorPermissionLogic
from kawaz.core.publishments.perms import PublishmentPermissionLogic
add_permission_logic(StarTestArticle, PublishmentPermissionLogic())
add_permission_logic(StarTestArticle, KawazAuthorPermissionLogic())
