# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.db import models


class CommentTestArticle(models.Model):
    text = models.CharField('text', max_length=30)
    class Meta:
        app_label = 'comments'

