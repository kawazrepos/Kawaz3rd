from django.views.generic import RedirectView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http.response import (HttpResponseRedirect,
                                  HttpResponseForbidden,
                                  HttpResponseNotAllowed)
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from permission.decorators import permission_required

from .forms import ProjectCreateForm
from .forms import ProjectUpdateForm
from .models import Project


@permission_required('projects.add_project')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectCreateForm

    def form_valid(self, form):
        # 管理者を自動指定
        form.instance.administrator = self.request.user
        return super().form_valid(form)


@permission_required('projects.change_project')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectUpdateForm


@permission_required('projects.delete_project')
class ProjectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('projects_project_list')


@permission_required('projects.view_project')
class ProjectDetailView(DetailView):
    model = Project


@permission_required('projects.view_project')
class ProjectListView(ListView):
    model = Project

    def get_queryset(self):
        return Project.objects.published(self.request.user)


@permission_required('projects.join_project')
class ProjectJoinView(SingleObjectMixin, RedirectView):
    """
    メンバーが参加する際に使用するView
    """
    http_method_names = ['post']
    permanent = False
    model = Project

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.join(request.user)
        return super().post(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return self.object.get_absolute_url()


@permission_required('projects.quit_project')
class ProjectQuitView(SingleObjectMixin, RedirectView):
    """
    メンバーが退会する際に使用するView
    """
    http_method_names = ['post']
    permanent = False
    model = Project

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.quit(request.user)
        return super().post(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return self.object.get_absolute_url()

