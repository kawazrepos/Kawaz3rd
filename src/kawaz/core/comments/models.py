

from django_comments.models import Comment

from .activity import CommentActivityMediator
from activities.registry import registry
registry.register(Comment, CommentActivityMediator())

from permission import add_permission_logic
from .perms import CommentPermissionLogic
add_permission_logic(Comment, CommentPermissionLogic())
