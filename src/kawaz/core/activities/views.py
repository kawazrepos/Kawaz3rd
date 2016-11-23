from permission.decorators import permission_required



from django.views.generic.list import ListView
from activities.models import Activity

class ActivityListView(ListView):
    paginate_by = 10
    model = Activity

    def get_queryset(self):
        type = self.request.GET.get('type', None)
        if type == 'wall':
            return Activity.objects.latests()
        return super().get_queryset()
