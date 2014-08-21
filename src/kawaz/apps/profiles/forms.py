from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _
from django.forms import widgets
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin, Bootstrap3InlineFormHelperMixin
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton

from .models import Profile
from .models import Skill
from .models import Account


class ProfileForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):
    form_tag = False

    skills = forms.ModelMultipleChoiceField(
        widget=widgets.CheckboxSelectMultiple,
        queryset=Skill.objects.all().order_by('pk'), required=False)
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


AccountFormSet = inlineformset_factory(Profile, Account, form=AccountForm,
                                       extra=1, can_delete=True)
