import os
from django.views.generic.base import TemplateView


class AnonymousIndexView(TemplateView):
    base_dir = 'core'
    template_name = os.path.join(base_dir, 'anonymous_index.html')


class AuthenticatedIndexView(TemplateView):
    base_dir = 'core'
    template_name = os.path.join(base_dir, 'authenticated_index.html')


def get_index_view(request, *args, **kwargs):
    """
    ログイン状態によってViewを振り分けます
    """
    if request.user.is_authenticated():
        return AuthenticatedIndexView.as_view()(request, *args, **kwargs)
    return AnonymousIndexView.as_view()(request, *args, **kwargs)
