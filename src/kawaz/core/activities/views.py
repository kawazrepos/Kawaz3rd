from permission.decorators import permission_required

__author__ = 'giginet'

from django.views.generic.list import ListView
from activities.models import Activity
from kawaz.core.personas.perms import ChildrenPermissionLogic

#@permission_required('activities.view_activity')
class ActivityListView(ListView):
    paginate_by = 10
    model = Activity

    def get_queryset(self):
        type = self.request.GET.get('type', None)
        if type == 'wall':
            return Activity.objects.latests()
        return super().get_queryset()
