from django.contrib import admin
from .models import Category, Project

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class ProjectAdmin(admin.ModelAdmin):
    search_fields = ('title', 'body', 'administrator__username', 'administrator__nickname', 'category__label',)
admin.site.register(Project, ProjectAdmin)
