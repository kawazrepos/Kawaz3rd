from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from kawaz.core.forms.fields import MarkdownField
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin

from .models import Project

class ProjectCreateForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):

    body = MarkdownField(label=_('body'))

    class Meta:
        model = Project
        exclude = (
            'administrator',
            'members',
            'created_at',
            'updated_at',
        )


class ProjectUpdateForm(ProjectCreateForm):
    class Meta(ProjectCreateForm.Meta):
        exclude = ['slug',]
