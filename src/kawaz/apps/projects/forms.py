from django import forms
from django.forms import ModelForm
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixin import Bootstrap3HorizontalFormMixin

from .models import Project

class ProjectCreateForm(Bootstrap3HorizontalFormMixin, ModelForm):

    body = forms.CharField(widget=MaceEditorWidget)

    class Meta:
        model = Project


class ProjectUpdateForm(ProjectCreateForm):
    class Meta(ProjectCreateForm.Meta):
        exclude = ['slug',]
