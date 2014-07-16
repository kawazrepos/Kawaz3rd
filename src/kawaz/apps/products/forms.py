from django import forms
from django.forms import ModelForm
from kawaz.core.forms.widgets import MaceEditorWidget
from django.forms import widgets
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from .models import Product
from .models import Platform
from .models import Category
from .models import Screenshot
from .models import PackageRelease
from .models import URLRelease


class ProductBaseForm(ModelForm):
    platforms = forms.ModelMultipleChoiceField(
        widget=widgets.CheckboxSelectMultiple,
        queryset=Platform.objects.all().order_by('pk'))
    categories = forms.ModelMultipleChoiceField(
        widget=widgets.CheckboxSelectMultiple,
        queryset=Category.objects.all().order_by('pk'))
    description = forms.CharField(widget=MaceEditorWidget)
    publish_at = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Product


class ProductCreateForm(ProductBaseForm):

    class Meta(ProductBaseForm.Meta):
        exclude = ('administrators', 'display_mode')


class ProductUpdateForm(ProductBaseForm):

    class Meta(ProductBaseForm.Meta):
        exclude = (
            'slug',
            'administrators', 'display_mode'
        )


class ScreenshotForm(ModelForm):

    class Meta:
        model = Screenshot
        fields = ('image',)


class PackageReleaseForm(ModelForm):

    class Meta:
        model = PackageRelease
        fields = (
            'label', 'platform',
            'version', 'file_content',
        )


class URLReleaseForm(ModelForm):

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
