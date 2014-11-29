from django.contrib import admin
from .models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    search_fields = ('title', 'body', 'author__username', 'author__nickname')
admin.site.register(Announcement, AnnouncementAdmin)
