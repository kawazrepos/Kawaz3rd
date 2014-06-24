from django import forms
from django.forms import widgets
from django.forms import ModelForm
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from .models import Product
from .models import Platform
from .models import Category
from .models import Screenshot

class ProductBaseForm(ModelForm):
    platforms = forms.ModelMultipleChoiceField(widget=widgets.CheckboxSelectMultiple,
                                               queryset=Platform.objects.all().order_by('pk'))
    categories = forms.ModelMultipleChoiceField(widget=widgets.CheckboxSelectMultiple,
                                                queryset=Category.objects.all().order_by('pk'))

    class Meta:
        model = Product

class ProductCreateForm(ProductBaseForm):
    class Meta(ProductBaseForm.Meta):
        exclude = ('description_markup_type', 'administrators', 'display_mode')

class ProductUpdateForm(ProductBaseForm):
    class Meta(ProductBaseForm.Meta):
        exclude = (
                'description_markup_type', 'slug', 
                'administrators', 'display_mode'
            )

class ScreenshotForm(ModelForm):
    class Meta:
        model = Screenshot
        fields = ('image',)

ScreenshotFormSet = inlineformset_factory(Product, Screenshot, extra=1, can_delete=True)

def get_screenshot_formset(form, formset=BaseInlineFormSet, *args, **kwargs):
    return inlineformset_factory(Product, Screenshot, form, formset, **kwargs)