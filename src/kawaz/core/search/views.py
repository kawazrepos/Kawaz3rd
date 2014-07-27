from django.views.generic import TemplateView
from .forms import KawazSearchForm

class SearchView(TemplateView):
    template_name = 'search/search.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = KawazSearchForm(self.request.GET)
        context['results'] = form.search()
        return context
