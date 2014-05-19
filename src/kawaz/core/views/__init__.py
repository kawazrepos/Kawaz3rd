import os
from django.views.generic.base import TemplateView
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser

from kawaz.apps.products.models import Product
from kawaz.apps.events.models import Event
from kawaz.apps.blogs.models import Entry
from kawaz.apps.announcements.models import Announcement

class AnonymousIndexView(TemplateView):
    base_dir = 'core'
    template_name = os.path.join(base_dir, 'anonymous_index.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured = Q(display_mode='featured')
        tiled = Q(display_mode='tiled')
        # ログインユーザーが非ログイントップを見ても必ず公開記事のみを返します
        user = AnonymousUser()
        context['recent_products'] = Product.objects.filter(display_mode='normal').order_by('-publish_at')[:3]
        context['featured_products'] = Product.objects.filter(featured).order_by('-publish_at')
        context['products'] = Product.objects.filter(featured | tiled).order_by('-publish_at')
        context['entries'] = Entry.objects.published(user).order_by('-publish_at')[:5]
        context['events'] = Event.objects.active(user).order_by('-start_period')[:5]
        context['announcements'] = Announcement.objects.published(user).order_by('-created_at')[:5]
        return context

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
