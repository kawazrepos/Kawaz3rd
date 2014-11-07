from django.utils.translation import ugettext as _
from django_filters import filters, FilterSet
from kawaz.core.filters.widgets import ListGroupLinkWidget
from kawaz.core.personas.profiles.models import Skill
from .models import Persona


class PersonaFilter(FilterSet):
    skills = filters.ModelChoiceFilter(
        name='_profile__skills',
        label=_('Skills'),
        queryset=Skill.objects.all(),
        widget=ListGroupLinkWidget(choices=[('', _('All'))])
    )

    class Meta:
        model = Persona
