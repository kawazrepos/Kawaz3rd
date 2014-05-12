from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from .forms import ProjectCreateForm
from .forms import ProjectUpdateForm

from .models import Project

from permission.decorators import permission_required

@permission_required('projects.add_project')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectCreateForm

    def form_valid(self, form):
        form.instance.administrator = self.request.user
        return super().form_valid(form)


@permission_required('projects.change_project')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectUpdateForm


@permission_required('projects.delete_project')
class ProjectDeleteView(DeleteView):
    model = Project


@permission_required('projects.view_project')
class ProjectDetailView(DetailView):
    model = Project


class ProjectListView(ListView):
    model = Project

    def get_queryset(self):
        return Project.objects.published(self.request.user)
