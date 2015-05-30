from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer_name', 'get_pub_state_display', 'period_start', 'number_of_attendees', 'created_at', 'updated_at')
    search_fields = ('title', 'body', 'organizer__username', 'organizer__nickname', 'category__label', 'place')

    def organizer_name(self, obj):
        return obj.organizer.nickname

    def number_of_attendees(self, obj):
        return obj.attendees.count()

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'organizer', None) is None:
            obj.organizer = request.user
        obj.save()

admin.site.register(Event, EventAdmin)
