# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Activity


class ActivityAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('status', 'remarks')}),
        (_('Target'), {'fields': ('content_type', 'object_id')}),
    )

    list_display = (
        'pk', 'created_at', 'status',
        'get_content_object'
    )
    list_filter = (
        'status', 'content_type',
    )
    search_fields = (
        'status', 'remarks',
        'get_content_object',
    )

    def get_content_object(self, obj):
        return obj._content_object
    get_content_object.short_description = _('Content object')

admin.site.register(Activity, ActivityAdmin)
