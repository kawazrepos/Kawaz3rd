from django.forms import ModelForm

from .models import Project

class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project


class ProjectUpdateForm(ProjectCreateForm):
    class Meta(ProjectCreateForm.Meta):
        exclude = ['slug',]
