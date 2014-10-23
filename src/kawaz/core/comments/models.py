__author__ = 'giginet'

from django_comments.models import Comment

from .activity import CommentActivityMediator
from activities.registry import registry
registry.register(Comment, CommentActivityMediator())
