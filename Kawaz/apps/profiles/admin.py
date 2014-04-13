from django.contrib import admin
from .models import Profile, Skill, Service, Account

class SkillAdmin(admin.ModelAdmin):
    pass
admin.site.register(Skill, SkillAdmin)

class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile, ProfileAdmin)

class ServiceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Service, ServiceAdmin)

class AccountAdmin(admin.ModelAdmin):
    pass
admin.site.register(Account, AccountAdmin)