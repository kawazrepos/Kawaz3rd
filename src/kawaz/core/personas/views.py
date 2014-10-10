# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/9
#
from django.http import HttpResponseNotAllowed
from django.utils.translation import ugettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from permission.decorators import permission_required
from kawaz.core.personas.forms import PersonaUpdateForm, PersonaRoleForm
from kawaz.core.personas.models import Persona

__author__ = 'giginet'

@permission_required('personas.change_persona')
class PersonaUpdateView(SuccessMessageMixin, UpdateView):
    model = Persona
    form_class = PersonaUpdateForm
    template_name = 'registration/persona_form.html'

    def get_success_message(self, cleaned_data):
        return _('Your user information successfully updated.')

    def get_object(self, queryset=None):
        return self.request.user


class AssignRoleMixin(SuccessMessageMixin):
    form_class = PersonaRoleForm
    role = None

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed()

    def get_form_kwargs(self):
        return {'role': self.role}

    def get_object(self, queryset=None):
        return self.request.user

@permission_required('personas.assign_role_persona')
class PersonaAssignAdamView(AssignRoleMixin, UpdateView):
    """
    神になるボタン
    """
    role = 'adam'

    def get_success_message(self, cleaned_data):
        return _("""Your role is changed to 'adam'""")


@permission_required('personas.assign_role_persona')
class PersonaAssignSeeleView(AssignRoleMixin, UpdateView):
    """
    神をやめるボタン
    """
    role = 'seele'

    def get_success_message(self, cleaned_data):
        return _("""Your role is changed to 'seele'""")
