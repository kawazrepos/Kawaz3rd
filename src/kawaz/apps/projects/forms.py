from django import forms
from django.forms import ModelForm
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin

from .models import Project

class ProjectCreateForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):

    body = forms.CharField(label=Project._meta.get_field('body').verbose_name, widget=MaceEditorWidget)

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
