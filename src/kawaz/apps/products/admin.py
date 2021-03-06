from django.contrib import admin
from .models import Category
from .models import Platform
from .models import Product
from .models import PackageRelease
from .models import URLRelease
from .models import Screenshot


class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)


class PlatformAdmin(admin.ModelAdmin):
    pass
admin.site.register(Platform, PlatformAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'last_modifier_nickname', 'get_display_mode_display', 'published_at', 'created_at', 'updated_at')

    def last_modifier_nickname(self, obj):
        if not obj.last_modifier:
            return '(未編集)'
        return obj.last_modifier.nickname

admin.site.register(Product, ProductAdmin)


class PackageReleaseAdmin(admin.ModelAdmin):
    readonly_fields = ('downloads',)
    search_fields = ('title', 'description',)
    list_display = ('label', 'platform', 'version', 'downloads')
admin.site.register(PackageRelease, PackageReleaseAdmin)


class URLReleaseAdmin(admin.ModelAdmin):
    readonly_fields = ('pageview',)
    list_display = ('label', 'platform', 'version', 'url', 'pageview')
admin.site.register(URLRelease, URLReleaseAdmin)


class ScreenshotAdmin(admin.ModelAdmin):
    pass
admin.site.register(Screenshot, ScreenshotAdmin)

