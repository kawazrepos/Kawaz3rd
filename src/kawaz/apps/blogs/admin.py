from django.contrib import admin
from .models import Entry
from kawaz.apps.stars.models import Star

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_nickname', 'get_pub_state_display', 'star_count', 'created_at', 'updated_at')
    search_fields = ('title', 'body', 'author__username', 'author__nickname', 'category__label')

    def author_nickname(self, obj):
        return obj.author.nickname

    def star_count(self, obj):
        stars = Star.objects.get_for_object(obj)
        return stars.count()


admin.site.register(Entry, EntryAdmin)

# Register your models here.
