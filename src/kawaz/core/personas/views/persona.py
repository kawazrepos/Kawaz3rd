from django.contrib import messages
from django.http import (HttpResponseNotAllowed,
                         HttpResponseRedirect,
                         Http404)
from django.utils.translation import ugettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django_filters.views import FilterView
from permission.decorators import permission_required
from ..forms import PersonaUpdateForm
from ..models import Persona
from ..models import Service
from ..filters import PersonaFilter


class PersonaDetailView(DetailView):
    model = Persona
    slug_field = 'username'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude(is_active=False)
        qs = qs.exclude(_profile=None)
        qs = qs.exclude(role='wille')
        qs = qs.prefetch_related(
            '_profile',
            '_profile__skills',
            '_profile__accounts__service',
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user = self.request.user
        if user.has_perm('personas.view_profile', self.object._profile):
            # アクセスユーザーは対象ユーザーのプロフィールを見る権限を所有
            # しているので `profile` というコンテキストにプロフィール実体
            # を渡す（アンダーバーから始まっているためテンプレートにて
            # `{{ object._profile }}`というようなアクセスは出来ない）
            # これはヒューマンエラーによるテンプレートでのプライベートな
            # プロフィール参照を避けるための仕様である
            context['profile'] = self.object._profile
        return context


class PersonaListView(FilterView):
    model = Persona
    filterset_class = PersonaFilter
    template_name_suffix = '_list'
    paginate_by = 24

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude(is_active=False)
        qs = qs.exclude(_profile=None)
        qs = qs.exclude(role='wille')
        qs = qs.prefetch_related(
            '_profile',
            '_profile__skills',
            '_profile__accounts__service',
        )
        qs = qs.order_by('-last_login')
        return qs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['all_services'] = Service.objects.all()
        return data


class PersonaGraveView(ListView):
    template_name = 'personas/persona_grave.html'

    def get_queryset(self):
        return Persona.objects.ghosts()


@permission_required('personas.change_persona')
class PersonaUpdateView(SuccessMessageMixin, UpdateView):
    model = Persona
    form_class = PersonaUpdateForm
    template_name = 'personas/persona_form.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude(is_active=False)
        qs = qs.exclude(_profile=None)
        qs = qs.exclude(role='wille')
        qs = qs.prefetch_related(
            '_profile',
            '_profile__skills',
            '_profile__accounts__service',
        )
        return qs

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated():
            raise Http404(
                _("Anonymous user does not have a persona update view")
            )
        qs = queryset or self.get_queryset()
        return get_object_or_404(qs, pk=self.request.user.pk)

    def get_success_message(self, cleaned_data):
        return _('Your user information was successfully updated.')


class AssignRoleMixin(object):
    model = Persona
    role = None

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.exclude(is_active=False)
        qs = qs.exclude(_profile=None)
        qs = qs.exclude(role='wille')
        return qs

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated():
            raise Http404(
                _("Anonymous user does not have an assign role view")
            )
        qs = queryset or self.get_queryset()
        return get_object_or_404(qs, pk=self.request.user.pk)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST',])

    @permission_required('personas.assign_role_persona')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.role = self.role
        self.object.save()
        messages.success(request, self.get_success_message({}))
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.get_object().get_absolute_url()

    def get_success_message(self, cleaned_data):
        return _("Your role is changed to '%(role)s'" % {
            'role': self.role.capitalize()
        })


class PersonaAssignAdamView(AssignRoleMixin, UpdateView):
    """アダムに昇格するためのビュー"""
    role = 'adam'


class PersonaAssignSeeleView(AssignRoleMixin, UpdateView):
    """ゼーレに降格するためのビュー"""
    role = 'seele'
