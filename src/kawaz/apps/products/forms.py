from django import forms
from django.forms import ModelForm
from kawaz.core.forms.fields import MarkdownField
from kawaz.core.forms.widgets import MaceEditorWidget
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin
from kawaz.core.forms.mixins import Bootstrap3InlineFormHelperMixin
from django.forms import widgets
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _
from .models import Product
from .models import Platform
from .models import Category
from .models import Screenshot
from .models import PackageRelease
from .models import URLRelease


class ProductBaseForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):
    form_tag = False

    body = MarkdownField(label=_('Body'))

    platforms = forms.ModelMultipleChoiceField(
        label=_('Platforms'),
        widget=widgets.CheckboxSelectMultiple,
        queryset=Platform.objects.all().order_by('pk'))
    categories = forms.ModelMultipleChoiceField(
        label=_('Categories'),
        widget=widgets.CheckboxSelectMultiple,
        queryset=Category.objects.all().order_by('pk'))
    description = forms.CharField(label=_('Description'), widget=MaceEditorWidget)
    publish_at = forms.DateField(label=_('Publish at'), widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Product
        exclude = ()

    def get_additional_objects(self):
        # Saveボタンを描画しない
        return []

class ProductCreateForm(ProductBaseForm):

    class Meta(ProductBaseForm.Meta):
        exclude = ('administrators', 'display_mode')


class ProductUpdateForm(ProductBaseForm):

    class Meta(ProductBaseForm.Meta):
        exclude = (
            'slug',
            'administrators', 'display_mode'
        )


class ScreenshotForm(Bootstrap3InlineFormHelperMixin, ModelForm):
    form_tag = False

    class Meta:
        model = Screenshot
        fields = ('image',)


class PackageReleaseForm(Bootstrap3InlineFormHelperMixin, ModelForm):
    form_tag = False

    class Meta:
        model = PackageRelease
        fields = (
            'label', 'platform',
            'version', 'file_content',
        )


class URLReleaseForm(Bootstrap3InlineFormHelperMixin, ModelForm):
    form_tag = False

    class Meta:
        model = URLRelease
        fields = (
            'label', 'platform',
            'version', 'url',
        )


ScreenshotFormSet = inlineformset_factory(Product, Screenshot,
                                          ScreenshotForm,
                                          extra=1, can_delete=True)
PackageReleaseFormSet = inlineformset_factory(Product, PackageRelease,
                                              PackageReleaseForm,
                                              extra=1, can_delete=True)
URLReleaseFormSet = inlineformset_factory(Product, URLRelease,
                                          URLReleaseForm,
                                          extra=1, can_delete=True)
