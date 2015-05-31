from django.contrib import admin
from .models import Material

class MaterialAdmin(admin.ModelAdmin):
    readonly_fields = ('slug', 'author', 'ip_address', 'created_at',)
    list_display = ('filename', 'slug', 'author_nickname', 'created_at')

    def author_nickname(self, obj):
        return obj.author.nickname

    search_fields = ('author__username', 'author__nickname')
admin.site.register(Material, MaterialAdmin)
