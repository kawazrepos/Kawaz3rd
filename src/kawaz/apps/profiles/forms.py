from django.forms import ModelForm

from .models import Profile
from .models import Account

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['remarks_markup_type']

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = (
            'service',
            'username',
            'pub_state'
        )
        exclude = ('user',)
