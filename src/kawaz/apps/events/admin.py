from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'organizer', None) is None:
            obj.organizer = request.user
        obj.save()

admin.site.register(Event, EventAdmin)
