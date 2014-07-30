from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    readonly_fields = ('gcal_id',)
admin.site.register(Event, EventAdmin)
