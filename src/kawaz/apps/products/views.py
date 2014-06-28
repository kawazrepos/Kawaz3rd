from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.core.urlresolvers import reverse_lazy

from django.forms.models import modelformset_factory

from permission.decorators import permission_required

from .forms import ProductCreateForm, ProductUpdateForm
from .forms import PackageReleaseForm, URLReleaseForm, ScreenshotForm
from .models import Product
from .models import PackageRelease, URLRelease, Screenshot


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product


class ProductFormSetMixin(object):

    def _get_formset(self, model, form_class):
        FormSet = modelformset_factory(model, form=form_class, extra=1, can_delete=True)
        return FormSet

    def get_url_release_formset(self):
        return self._get_formset(URLRelease, URLReleaseForm)

    def get_package_release_formset(self):
        return self._get_formset(PackageRelease, PackageReleaseForm)

    def get_screenshot_formset(self):
        return self._get_formset(Screenshot, ScreenshotForm)

class ProductFormMixin(ProductFormSetMixin):
    def post(self, request, *args, **kwargs):
        # formsetの中身も保存するために複雑なことをしている
        # ToDo 実装上の問題を抱えているから後で直す
        try:
            self.object = self.get_object()
        except:
            self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # URLRelease, PackageRelease, Screenshotの3つのFormSetを処理する
        URLReleaseFormSet = self.get_url_release_formset()
        PackageReleaseFormSet = self.get_package_release_formset()
        ScreenshotFormSet = self.get_screenshot_formset()

        url_release_formset = URLReleaseFormSet(request.POST, request.FILES, prefix='url_releases')
        package_release_formset = PackageReleaseFormSet(request.POST, request.FILES, prefix='package_releases')
        screenshot_formset = ScreenshotFormSet(request.POST, request.FILES, prefix='screenshots')

        if form.is_valid() \
                and url_release_formset.is_valid() \
                and package_release_formset.is_valid() \
                and screenshot_formset.is_valid():
            formsets = (url_release_formset,)
            r = self.form_valid(form)
            for formset in formsets:
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.product = self.object
                    instance.save()
            return r
        else:
            print("invalid")
            return self.form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # formsetを作成して渡す
        URLReleaseFormSet = self.get_url_release_formset()
        PackageReleaseFormSet = self.get_package_release_formset()
        ScreenshotFormSet = self.get_screenshot_formset()

        context['url_release_formset'] = URLReleaseFormSet(prefix='url_releases')
        context['package_release_formset'] = PackageReleaseFormSet(prefix='package_releases')
        context['screenshot_formset'] = ScreenshotFormSet(prefix='screenshots')

        return context


@permission_required('products.add_product')
class ProductCreateView(ProductFormMixin, CreateView):
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
class ProductUpdateView(ProductFormMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm


@permission_required('products.delete_product')
class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products_product_list')
