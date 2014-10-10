# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/9
#
from django.utils.translation import ugettext as _
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from permission.decorators import permission_required
from kawaz.core.personas.forms import PersonaUpdateForm
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
