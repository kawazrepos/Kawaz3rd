from django.conf.urls import patterns, url

from .views import ProductListView
from .views import ProductUpdateView
from .views import ProductCreateView
from .views import ProductDeleteView
from .views import ProductDetailView
from .views import ProductPreview
from .views import PackageReleaseDetailView
from .views import URLReleaseDetailView

urlpatterns = patterns('',
    url('^$',
        ProductListView.as_view(), name='products_product_list'),
    url('^preview/$',
        ProductPreview.as_view(), name='products_product_preview'),
    url('^create/$',
        ProductCreateView.as_view(), name='products_product_create'),
    url('^(?P<pk>\d+)/update/$',
        ProductUpdateView.as_view(), name='products_product_update'),
    url('^(?P<pk>\d+)/delete/$',
        ProductDeleteView.as_view(), name='products_product_delete'),
    url('^(?P<slug>[\w_-]+)/$',
        ProductDetailView.as_view(), name='products_product_detail'),
    url('^package_releases/(?P<pk>\d+)/$',
        PackageReleaseDetailView.as_view(), name='products_package_release_detail'),
    url('^url_releases/(?P<pk>\d+)/$',
        URLReleaseDetailView.as_view(), name='products_url_release_detail'),
)
