from django.contrib import admin
from .models import RecentActivity

class RecentActivityAdmin(admin.ModelAdmin):
    pass
admin.site.register(RecentActivity, RecentActivityAdmin)
