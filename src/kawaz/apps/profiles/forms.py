from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixin import Bootstrap3HorizontalFormHelperMixin, Bootstrap3InlineFormHelperMixin
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton

from .models import Profile
from .models import Account


class ProfileForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):
    form_tag = False

    remarks = forms.CharField(widget=MaceEditorWidget)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)

    class Meta:
        model = Profile

    def get_additional_objects(self):
        # Saveボタンを描画しない
        return []


class AccountForm(Bootstrap3InlineFormHelperMixin, ModelForm):
    form_tag = False

    class Meta:
        model = Account
        fields = (
            'service',
            'username',
            'pub_state',
        )
        exclude = ('user',)

    def get_helper(self):
        helper = self.helper_class()
        helper.template = 'formset.html'
        helper.layout = Layout(
            'username',
            StrictButton(_('Delete'))
        )
        return helper


AccountFormSet = inlineformset_factory(Profile, Account, form=AccountForm,
                                       extra=1, can_delete=True)
