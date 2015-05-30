from django.contrib import admin
from .models import Category, Project

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_status_display', 'administrator_nickname', 'created_at', 'updated_at')

    def administrator_nickname(self, obj):
        return obj.administrator.nickname

    search_fields = ('title', 'body', 'administrator__username', 'administrator__nickname', 'category__label',)
admin.site.register(Project, ProjectAdmin)
