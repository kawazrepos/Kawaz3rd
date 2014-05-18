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
    pass
admin.site.register(Product, ProductAdmin)


class PackageReleaseAdmin(admin.ModelAdmin):
    pass
admin.site.register(PackageRelease, PackageReleaseAdmin)


class URLReleaseAdmin(admin.ModelAdmin):
    pass
admin.site.register(URLRelease, URLReleaseAdmin)


class ScreenshotAdmin(admin.ModelAdmin):
    pass
admin.site.register(Screenshot, ScreenshotAdmin)

