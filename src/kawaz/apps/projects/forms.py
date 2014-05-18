from django.forms import ModelForm

from .models import Project

class ProjectCreateForm(ModelForm):
    class Meta:
        model = Project
        exclude = ['body_markup_type']


class ProjectUpdateForm(ProjectCreateForm):
    class Meta(ProjectCreateForm.Meta):
        exclude = ['body_markup_type', 'slug']
