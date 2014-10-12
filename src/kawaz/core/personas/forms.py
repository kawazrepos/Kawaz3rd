# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django import forms
from django.forms.widgets import RadioFieldRenderer
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from kawaz.core.forms.widgets import RadioSelectWithHelpText
from .models import Persona



class PersonaCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    # Ref: https://groups.google.com/forum/#!topic/django-users/kOVEy9zYn5c
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            # Not sure why UserCreationForm doesn't do this in the first place,
            # or at least test to see if _meta.model is there and if not use User...
            self._meta.model._default_manager.get(username=username)
        except self._meta.model.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta:
        model = Persona
        exclude = (
            'role',
        )


class PersonaAdminUpdateForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    class Meta:
        model = Persona
        exclude = (
            'role',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'role' in self.fields:
            choices = Persona.ROLE_TYPES
            choices_help_texts = (
                _("Users in this role have all permissions"),
                _("Users in this role can promote to the adam"),
                _("Users in this role have staff permission"),
                _("Users in this role are assumed to be a member of the site"),
                _("Users in this role are assumed to be a signed in visitor"),
            )
            self.fields['role'].widget = RadioSelectWithHelpText(
                    choices=choices, help_texts=choices_help_texts)

class PersonaUpdateForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = (
            'last_name',
            'first_name',
            'email',
            'nickname',
            'avatar',
            'quotes',
            'gender',
        )
        exclude = (
            'password',
            'role',
            'username',
        )

class PersonaRoleForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ('role',)