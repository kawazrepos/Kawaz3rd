# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from historywall.mediator import Mediator


class ProductWallMediator(Mediator):
    include_fields = (
        'title',
        'description',
        'thumbnail',
        'trailer',
        'comments',
        'urlreleasesss',
        'packagereleasess',
        'screenshots',
    )
