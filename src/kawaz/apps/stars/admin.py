from django.contrib import admin
from .models import Star

class StarAdmin(admin.ModelAdmin):
    pass
admin.site.register(Star, StarAdmin)
