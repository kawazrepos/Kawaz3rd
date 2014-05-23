from django.contrib import admin
from .models import Material

class MaterialAdmin(admin.ModelAdmin):
    pass
admin.site.register(Material, MaterialAdmin)
