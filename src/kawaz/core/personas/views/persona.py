from django.contrib import messages
from django.http import (HttpResponseNotAllowed,
                         HttpResponseRedirect,
                         HttpResponseForbidden,
                         Http404)
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django_filters.views import FilterView
from permission.decorators import permission_required
from ..forms import PersonaUpdateForm, PersonaRoleForm
from ..models import Persona
from ..filters import PersonaFilter


class PersonaDetailView(DetailView):
    model = Persona
    slug_field = 'username'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related(
            '_profile',
            '_profile__skills',
            '_profile__accounts__service',
        )
        return qs.exclude(role='wille')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        # アクセスユーザーが対象ユーザーのプロフィールにアクセスする権限の
        # 有無により'profile'コンテキストを渡すか否かを決定する
        user = self.get_object()
        try:
            if self.request.user.has_perm('personas.view_profile', user._profile):
                context['profile'] = user._profile
        except ObjectDoesNotExist:
            # 通常ユーザーはProfileを持つはずだが依存性を下げるためにここは
            # Fail silently で扱っている
            pass
        return context


class PersonaListView(FilterView):
    model = Persona
    filterset_class = PersonaFilter
    template_name_suffix = '_list'
    paginate_by = 24

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related(
            '_profile',
            '_profile__skills',
            '_profile__accounts__service',
        )
        qs = qs.order_by('-last_login')
        return qs.exclude(role='wille')


@permission_required('personas.change_persona')
class PersonaUpdateView(SuccessMessageMixin, UpdateView):
    model = Persona
    form_class = PersonaUpdateForm
    template_name = 'personas/persona_form.html'

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related(
            '_profile',
            '_profile__skills',
            '_profile__accounts__service',
        )
        return qs.exclude(role='wille')

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated():
            raise Http404(
                _("Anonymouse user does not have a persona update view")
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
        return qs.exclude(role='wille')

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated():
            raise Http404(
                _("Anonymouse user does not have an assign role view")
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
