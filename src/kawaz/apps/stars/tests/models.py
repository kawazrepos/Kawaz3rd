# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models
from kawaz.core.personas.models import Persona
from kawaz.core.permissions.logics import PUB_STATES


class StarTestArticle(models.Model):
    pub_state = models.CharField('Publish State', choices=PUB_STATES,
                                 max_length=10, default='public')
    author = models.ForeignKey(Persona)
    title = models.CharField('Title', max_length=30)

    class Meta:
        app_label = 'stars'
        permissions = (
            ('view_startestarticle', 'Can view the articles'),
        )


from permission import add_permission_logic
from permission.logics.author import AuthorPermissionLogic
from kawaz.core.permissions.logics import PubStatePermissionLogic
add_permission_logic(StarTestArticle, PubStatePermissionLogic())
add_permission_logic(StarTestArticle, AuthorPermissionLogic())
