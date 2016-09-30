def get_form():
    from kawaz.core.comments.forms import KawazCommentForm
    return KawazCommentForm

def get_model():
    from django_comments.models import Comment
    return Comment