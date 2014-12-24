from django import forms
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormTermsOfService, attrs_dict

class KawazRegistrationForm(RegistrationFormTermsOfService):
        username = forms.RegexField(regex=r'^[\w.@+-]+$',
                                    max_length=30,
                                    widget=forms.TextInput(attrs={'class': 'required',
                                                                  'placeholder': 'kawaz_tan'}),
                                    label=_("Username"),
                                    help_text=_(_("This value must contain "
                                                     "only letters, numbers and "
                                                     "underscores.")),
                                    error_messages={
                                        'invalid': _("This value must contain "
                                                     "only letters, numbers and "
                                                     "underscores.")
                                    })


__author__ = 'giginet'
