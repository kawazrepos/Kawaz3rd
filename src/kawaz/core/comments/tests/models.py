# coding=utf-8
"""
"""
from kawaz.core.personas.models import Persona

__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models


class CommentTestArticle(models.Model):
    text = models.CharField('text', max_length=30)
    author = models.ForeignKey(Persona)

    class Meta:
        app_label = 'comments'

from permission import add_permission_logic
from kawaz.core.personas.perms import RoleBasedAuthorPermissionLogic
add_permission_logic(CommentTestArticle, RoleBasedAuthorPermissionLogic())
