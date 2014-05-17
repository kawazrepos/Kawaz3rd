from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import DeleteView

from permission.decorators import permission_required

from .models import Product

@permission_required('products.add_product')
class ProductCreateView(CreateView):
    model = Product


@permission_required('products.change_product')
class ProductUpdateView(UpdateView):
    model = Product


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


@permission_required('products.delete_product')
class ProductDeleteView(DeleteView):
    model = Product
