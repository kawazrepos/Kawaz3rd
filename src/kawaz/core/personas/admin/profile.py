from django.contrib import admin
from ..models import Profile, Skill, Service, Account


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'birthday', 'place')

    def nickname(self, obj):
        return obj.user.nickname

    search_fields = ('address', 'remarks',)


class SkillAdmin(admin.ModelAdmin):
    pass


class ServiceAdmin(admin.ModelAdmin):
    pass


class AccountAdmin(admin.ModelAdmin):
    pass


admin.site.register(Skill, SkillAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Account, AccountAdmin)
