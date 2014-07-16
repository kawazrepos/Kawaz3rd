from django import forms
from django.forms import ModelForm
from kawaz.core.forms.widgets import MaceEditorWidget

from .models import Project

class ProjectCreateForm(ModelForm):

    body = forms.CharField(widget=MaceEditorWidget)

    class Meta:
        model = Project


class ProjectUpdateForm(ProjectCreateForm):
    class Meta(ProjectCreateForm.Meta):
        exclude = ['slug',]
