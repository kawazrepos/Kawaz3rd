from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Profile
from .models import Account


class ProfileForm(ModelForm):
    class Meta:
        model = Profile


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = (
            'service',
            'username',
            'pub_state'
        )
        exclude = ('user',)


AccountFormSet = inlineformset_factory(Profile, Account,
                                       extra=1, can_delete=True)
