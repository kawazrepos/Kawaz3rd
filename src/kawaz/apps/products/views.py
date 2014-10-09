from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import DeleteView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from django.forms.models import modelformset_factory

from django_filters.views import FilterView

from permission.decorators import permission_required

from .forms import ProductCreateForm, ProductUpdateForm
from .forms import PackageReleaseForm, URLReleaseForm, ScreenshotForm
from .forms import PackageReleaseFormSet, URLReleaseFormSet, ScreenshotFormSet
from kawaz.core.views.delete import DeleteNotificationView
from .models import Product
from .models import PackageRelease, URLRelease, Screenshot

from .filters import ProductFilter
from kawaz.core.views.preview import SingleObjectPreviewMixin

class ProductListView(FilterView):
    model = Product
    filterset_class = ProductFilter
    template_name_suffix = '_list'


class ProductDetailView(DetailView):
    model = Product


class ProductFormMixin(SuccessMessageMixin):

    def _get_formset(self, formset_class, **kwargs):
        if self.request.method in ('PUT', 'POST'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        if hasattr(self, 'object'):
            kwargs.update({
                'instance': self.object,
            })
        formset = formset_class(**kwargs)
        return formset

    def get_url_release_formset(self):
        return self._get_formset(URLReleaseFormSet,
                                 prefix='url_releases')

    def get_package_release_formset(self):
        return self._get_formset(PackageReleaseFormSet,
                                 prefix='package_releases')

    def get_screenshot_formset(self):
        return self._get_formset(ScreenshotFormSet,
                                 prefix='screenshots')

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # formsets
        url_release_formset = self.get_url_release_formset()
        package_release_formset = self.get_package_release_formset()
        screenshot_formset = self.get_screenshot_formset()
        return self.render_to_response(self.get_context_data(
            form=form,
            url_release_formset=url_release_formset,
            package_release_formset=package_release_formset,
            screenshot_formset=screenshot_formset,
        ))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        # formsets
        url_release_formset = self.get_url_release_formset()
        package_release_formset = self.get_package_release_formset()
        screenshot_formset = self.get_screenshot_formset()
        if (form.is_valid() and
                url_release_formset.is_valid() and
                package_release_formset.is_valid() and
                screenshot_formset.is_valid()):
            return self.form_valid(
                form,
                url_release_formset,
                package_release_formset,
                screenshot_formset,
            )
        else:
            return self.form_invalid(
                form,
                url_release_formset,
                package_release_formset,
                screenshot_formset,
            )

    def form_valid(self, form,
                   url_release_formset,
                   package_release_formset,
                   screenshot_formset):
        self.object = form.save()
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        # assign instance to all formsets
        formsets = (url_release_formset,
                    package_release_formset,
                    screenshot_formset)
        for formset in formsets:
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = self.object
                instance.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,
                     url_release_formset,
                     package_release_formset,
                     screenshot_formset):
        return self.render_to_response(self.get_context_data(
            form=form,
            url_release_formset=url_release_formset,
            package_release_formset=package_release_formset,
            screenshot_formset=screenshot_formset,
        ))


@permission_required('products.add_product')
class ProductCreateView(ProductFormMixin, CreateView):
    model = Product
    form_class = ProductCreateForm

    def form_valid(self, *args, **kwargs):
        response = super().form_valid(*args, **kwargs)
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

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        return _("""Product '{title}' successfully created.""".format(**{
            'title': cleaned_data['title']
        }))

@permission_required('products.change_product')
class ProductUpdateView(ProductFormMixin, UpdateView):
    model = Product
    form_class = ProductUpdateForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_message(self, cleaned_data):
        return _("""Product '{title}' successfully updated.""".format(**{
            'title': cleaned_data['title']
        }))


@permission_required('products.delete_product')
class ProductDeleteView(DeleteNotificationView):
    model = Product
    success_url = reverse_lazy('products_product_list')

    def get_success_message(self):
        return _("Product '{title}' successfully deleted.")


class ProductPreview(SingleObjectPreviewMixin, DetailView):
    model = Product
    template_name = "products/components/product_detail.html"
