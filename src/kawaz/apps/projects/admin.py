from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Category, Project


class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_status_display', 'administrator_nickname', 'created_at', 'updated_at', 'is_legacy')

    @staticmethod
    def administrator_nickname(obj):
        return obj.administrator.nickname
    administrator_nickname.short_description = _("Administrator's nickname")

    @staticmethod
    def is_legacy(obj):
        return obj.is_legacy
    is_legacy.short_description = _('Burned')

    search_fields = ('title', 'body', 'administrator__username', 'administrator__nickname', 'category__label',)
admin.site.register(Project, ProjectAdmin)
