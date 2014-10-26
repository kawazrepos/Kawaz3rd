from django.utils.translation import ugettext as _
from django_filters import filters, FilterSet
from kawaz.apps.profiles.models import Skill
from kawaz.core.filters.widgets import ListGroupLinkWidget
from .models import Persona


class PersonaFilter(FilterSet):
    skills = filters.ModelChoiceFilter(
        label=_('Skills'),
        queryset=Skill.objects.all(),
        widget=ListGroupLinkWidget(choices=[('', _('All'))])
    )

    class Meta:
        model = Persona
        fields = ['_profile__skills',]
