from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView

from .models import Project

from permission.decorators import permission_required

@permission_required('projects.add_project')
class ProjectCreateView(CreateView):
    model = Project


@permission_required('projects.edit_project')
class ProjectUpdateView(UpdateView):
    model = Project


@permission_required('projects.delete_project')
class ProjectDeleteView(DeleteView):
    model = Project


@permission_required('projects.view_project')
class ProjectDetailView(DetailView):
    model = Project


class ProjectListView(ListView):
    model = Project


class ProjectAuthorListView(ListView):
    model = Project


class ProjectCategoryListView(ListView):
    model = Project