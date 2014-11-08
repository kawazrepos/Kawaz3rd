from django.utils.translation import ugettext as _
from django_filters import filters, FilterSet
from kawaz.core.filters.widgets import ListGroupLinkWidget
from .models import Persona, Skill


class PersonaFilter(FilterSet):
    skills = filters.ModelChoiceFilter(
        name='_profile__skills',
        label=_('Skills'),
        queryset=Skill.objects.all(),
        widget=ListGroupLinkWidget(choices=[('', _('All'))])
    )

    class Meta:
        model = Persona
