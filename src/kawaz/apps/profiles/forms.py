from django.forms import ModelForm

from .models import Profile

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['remarks_markup_type']
