from django.conf.urls import url

from .views import ProductListView
from .views import ProductUpdateView
from .views import ProductCreateView
from .views import ProductDeleteView
from .views import ProductDetailView
from .views import ProductPreviewView
from .views import PackageReleaseDetailView
from .views import URLReleaseDetailView


urlpatterns = [
    url('^$',
        ProductListView.as_view(), name='products_product_list'),
    url('^preview/$',
        ProductPreviewView.as_view(), name='products_product_preview'),
    url('^create/$',
        ProductCreateView.as_view(), name='products_product_create'),
    url('^package_releases/(?P<pk>\d+)/$',
        PackageReleaseDetailView.as_view(),
        name='products_package_release_detail'),
    url('^url_releases/(?P<pk>\d+)/$',
        URLReleaseDetailView.as_view(),
        name='products_url_release_detail'),
    url('^(?P<slug>[\w_-]+)/$',
        ProductDetailView.as_view(), name='products_product_detail'),
    url('^(?P<slug>[\w_-]+)/update/$',
        ProductUpdateView.as_view(), name='products_product_update'),
    url('^(?P<slug>[\w_-]+)/delete/$',
        ProductDeleteView.as_view(), name='products_product_delete'),
]
