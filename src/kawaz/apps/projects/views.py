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
from kawaz.core.views.preview import SingleObjectPreviewMixin
from .models import Project


class ProjectArchiveView(ListView):
    """
    アーカイブ化されたプロジェクト閲覧用のビューです
    """
    template_name_suffix = '_archive'
    paginate_by = 50
    order_by = ('title', 'category', 'status', 'created_at',)

    def get_queryset(self):
        qs = Project.objects.archived(self.request.user)
        order_by = self.request.GET.get('o', '')
        if order_by in self.order_by:
            qs = qs.order_by(order_by)
        return qs


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

    def get_queryset(self):
        qs = super().get_queryset()
        qs.prefetch_related('members')
        return qs


@permission_required('projects.view_project')
class ProjectListView(ListView):
    model = Project

    def get_queryset(self):
        qs = Project.objects.published(self.request.user)
        qs.prefetch_related('members')
        return qs


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


class ProjectPreview(SingleObjectPreviewMixin, DetailView):
    model = Project
    template_name = "projects/components/project_detail.html"
