from django.contrib import admin
from .models import Profile, Skill

class SkillAdmin(admin.ModelAdmin):
    pass
admin.site.register(Skill, SkillAdmin)

class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile, ProfileAdmin)