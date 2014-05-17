from django.conf.urls import patterns, url

from .views import ProductListView
from .views import ProductUpdateView
from .views import ProductCreateView
from .views import ProductDeleteView
from .views import ProductDetailView

urlpatterns = patterns('',
    url('^$',                               ProductListView.as_view(),         name='products_product_list'),
    url('^create/$',                        ProductCreateView.as_view(),       name='products_product_create'),
    url('^(?P<pk>\d+)/update/$',            ProductUpdateView.as_view(),       name='products_product_update'),
    url('^(?P<pk>\d+)/delete/$',            ProductDeleteView.as_view(),       name='products_product_delete'),
    url('^(?P<slug>[\w_-]+)/$',             ProductDetailView.as_view(),       name='products_product_detail'),
)