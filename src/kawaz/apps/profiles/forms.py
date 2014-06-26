from django.forms import ModelForm
from django.forms.models import modelformset_factory

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

def get_account_formset():
    AccountFormSet = modelformset_factory(Account, form=AccountForm, extra=1, can_delete=True)
    return AccountFormSet
