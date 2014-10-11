from django.contrib import admin
from .models import HatenablogEntry

class HatenablogEntryAdmin(admin.ModelAdmin):
    pass
admin.site.register(HatenablogEntry, HatenablogEntryAdmin)
