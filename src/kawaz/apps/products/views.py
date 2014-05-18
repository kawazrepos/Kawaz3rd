from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse_lazy

from permission.decorators import permission_required

from .forms import ProductCreateForm, ProductUpdateForm

from .models import Product

@permission_required('products.add_product')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm

    def form_valid(self, form):
        # 作成時のユーザーを管理者に追加します
        # ToDo FIX ME
        instance = super().form_valid(form)
        form.instance.join(self.request.user)
        return instance

@permission_required('products.change_product')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductUpdateForm


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


@permission_required('products.delete_product')
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products_product_list')
