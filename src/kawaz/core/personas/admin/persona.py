from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from ..models import Persona
from ..forms import PersonaCreationForm
from ..forms import PersonaAdminUpdateForm


class PersonaAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('nickname', 'gender', 'avatar')}),
        (_('Extra info'), {'fields': ('quotes', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'role',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )
    form = PersonaAdminUpdateForm
    add_form = PersonaCreationForm
    list_display = ('nickname', 'username', 'email')
    list_filter = ('role', 'is_active', 'groups')
    search_fields = ('nickname', 'username', 'email', 'first_name', 'last_name', 'role')
    ordering = ('nickname', 'username', 'email',)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if not request.user.is_superuser:
            # ignore db permission because we are using logic based permissions
            readonly_fields.append('user_permissions')
        if not request.user.has_perm('personas.assign_role_persona', obj):
            readonly_fields.append('role')
        if not request.user.has_perm('personas.activate_persona', obj):
            readonly_fields.append('is_active')
        if not request.user.has_perm('personas.change_persona', obj):
            readonly_fields.extend([
                    'username', 'email',
                    'nickname', 'gender', 'avatar',
                    'quotes', 'first_name', 'last_name',
                    'groups',
                    'last_login', 'date_joined',
                ])
        return readonly_fields
admin.site.register(Persona, PersonaAdmin)
