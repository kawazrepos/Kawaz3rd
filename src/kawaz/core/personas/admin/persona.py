from copy import copy
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from ..models import Persona
from ..forms import PersonaCreationForm
from ..forms import PersonaAdminUpdateForm


class PersonaAdmin(UserAdmin):
    actions = None
    # 最終ログイン日での絞り込みを可能に
    date_hierarchy = 'last_login'
    # 追加変更ページでの項目を制御
    fieldsets = (
        (None, {
            'fields': (
                'is_active',
                'username', 'email',
                ('nickname', 'gender'),
                ('get_avatar_middle', 'avatar'),
                'quotes',
                'role',
            ),
        }),
        (_('Personal info'), {
            'fields': (
                ('last_name', 'first_name'),
                'groups',
            ),
        }),
    )
    radio_fields = {
        'role': admin.VERTICAL
    }
    list_display = (
        'get_display_name', 'role', 'email',
        'last_login', 'is_active',
    )
    list_filter = (
        'is_active',
        'role',
        'groups',
    )
    search_fields = (
        'username', 'email',
        'nickname',
        'first_name', 'last_name',
        'quotes',
    )
    ordering = (
        'username',
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if not request.user.has_perm('personas.assign_role_persona', obj):
            readonly_fields.append('role')
        if obj == request.user and 'role' not in readonly_fields:
            # ゼーレやスーパーユーザが間違えて自分の役職をゼーレ以下に下げて
            # しまうミスを防ぐため、自分自身の場合は役職変更を不可に
            readonly_fields.append('role')
        if not request.user.has_perm('personas.activate_persona', obj):
            readonly_fields.append('is_active')
        if not request.user.has_perm('personas.change_persona', obj):
            readonly_fields.extend((
                'username', 'email',
                'nickname', 'gender', 'avatar',
                'quotes', 'first_name', 'last_name',
                'groups',
            ))
        # 表示用メソッドを読み取り専用に指定
        readonly_fields.extend((
            'get_avatar_middle',
            'get_display_name',
        ))
        return readonly_fields

    def get_avatar_img(self, obj, size):
        return '<img src="{}" alt="avatar" />'.format(
            obj.get_avatar(size)
        )

    def get_avatar_middle(self, obj):
        return self.get_avatar_img(obj, 'middle')
    get_avatar_middle.short_description = _('Thumbnail')
    get_avatar_middle.allow_tags = True

    def get_display_name(self, obj):
        img = self.get_avatar_img(obj, 'small')
        return "{} @{} ({})".format(
            img, obj.username, obj.nickname,
        )
    get_display_name.short_description = _('Display name')
    get_display_name.allow_tags = True

admin.site.register(Persona, PersonaAdmin)
