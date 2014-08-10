from django.utils.translation import ugettext as _
import django_filters
from django_filters import filters
from .models import Profile
from .models import Skill
from kawaz.core.filters.widgets import ListGroupLinkWidget


class ProfileFilter(django_filters.FilterSet):
    skills = filters.ModelChoiceFilter(
        label=_('Skills'),
        queryset=Skill.objects.all(),
        widget=ListGroupLinkWidget(choices=[('', _('All'))]))

    class Meta:
        model = Profile
        fields = ['skills',]
