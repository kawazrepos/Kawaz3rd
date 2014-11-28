from django.contrib import admin
from .models import Entry

class EntryAdmin(admin.ModelAdmin):
    search_fields = ('title', 'body', 'author__username', 'author__nickname', 'category__label')
admin.site.register(Entry, EntryAdmin)

# Register your models here.
