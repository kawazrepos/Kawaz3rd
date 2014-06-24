from django import forms
from django.forms import widgets
from django.forms import ModelForm
from .models import Product
from .models import Platform
from .models import Category

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
