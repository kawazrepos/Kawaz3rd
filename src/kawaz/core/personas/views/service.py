from django.http import Http404
from django.views.generic.detail import DetailView
from ..models.profile import Service


class ServiceDetailView(DetailView):
    model = Service
    template_name = 'personas/service_detail.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['all_services'] = Service.objects.all()
        return data