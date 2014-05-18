from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse_lazy

from permission.decorators import permission_required

from .forms import ProductCreateForm, ProductUpdateForm
from .models import Product


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


@permission_required('products.add_product')
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object:
            # 作成に成功した場合は作成したユーザーを自動的に管理者に加える
            #
            # Note:
            #   これはManyToManyRelationになるためinstanceが存在しないと
            #   行えない。したがってまずインスタンスの生成を行なっている
            #   self.object は親の form_valid で設定される
            #
            self.object.join(self.request.user)
        return response


@permission_required('products.change_product')
class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductUpdateForm


@permission_required('products.delete_product')
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products_product_list')
