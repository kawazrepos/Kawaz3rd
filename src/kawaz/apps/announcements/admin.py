from django.contrib import admin
from .models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    pass
admin.site.register(Announcement, AnnouncementAdmin)
