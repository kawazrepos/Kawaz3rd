from django.contrib import admin
from .models import Category
from .models import PackageRelease
from .models import Platform
from .models import Product
from .models import ScreenShot
from .models import URLRelease

class CategoryAdmin(admin.ModelAdmin):
    pass
admin.site.register(Category, CategoryAdmin)

class PackageReleaseAdmin(admin.ModelAdmin):
    pass
admin.site.register(PackageRelease, PackageReleaseAdmin)

class PlatformAdmin(admin.ModelAdmin):
    pass
admin.site.register(Platform, PlatformAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)

class ScreenShotAdmin(admin.ModelAdmin):
    pass
admin.site.register(ScreenShot, ScreenShotAdmin)

class URLReleaseAdmin(admin.ModelAdmin):
    pass
admin.site.register(URLRelease, URLReleaseAdmin)
