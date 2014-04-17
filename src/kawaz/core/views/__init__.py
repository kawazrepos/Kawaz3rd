import os
from django.views.generic.base import View
from django.views.generic.base import TemplateView

class IndexView(TemplateView):
    base_dir = 'core'
    authenticated_template_name = os.path.join(base_dir, 'authenticated_index.html')
    anonymous_template_name = os.path.join(base_dir, 'anonymous_index.html')

    def get_template_names(self):
        # If user is authenticated, returns authenticated template else returns anonymous template
        if self.request.user.is_authenticated():
            return [self.authenticated_template_name]
        return [self.anonymous_template_name]