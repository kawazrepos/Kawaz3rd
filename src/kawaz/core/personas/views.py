from django.contrib import messages
from django.http import (HttpResponseNotAllowed,
                         HttpResponseRedirect,
                         HttpResponseForbidden)
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django_filters.views import FilterView
from permission.decorators import permission_required
from kawaz.core.personas.forms import PersonaUpdateForm, PersonaRoleForm
from kawaz.core.personas.models import Persona
from .filters import PersonaFilter


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
            if self.request.user.has_perm('profiles.view_profile', user._profile):
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
        return qs.exclude(role='wille')



@permission_required('personas.change_persona')
class PersonaUpdateView(SuccessMessageMixin, UpdateView):
    model = Persona
    slug_field = 'username'
    form_class = PersonaUpdateForm
    template_name = 'personas/persona_form.html'

    def get_success_message(self, cleaned_data):
        return _('Your user information was successfully updated.')


class AssignRoleMixin(object):
    model = Persona
    slug_field = 'username'
    role = None

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST',])

    @permission_required('personas.assign_role_persona')
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object != request.user:
            # Promote/Demote 機能は非常に危険な機能なためAdminでは他人に対し
            # Assign権限を持つゼーレやアダムでも自身以外に対するPromote/Demote
            # を行おうとした場合は Forbidden する
            return HttpResponseForbidden(_(
                "Promotin/Demotion is only allowed for your own account. "
                "If you required to assign role to a particuar user, use "
                "admin site (central-dogma) instead."
            ))
        else:
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
