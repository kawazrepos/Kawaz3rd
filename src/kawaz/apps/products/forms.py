from django.forms import ModelForm
from .models import Product

class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        exclude = ('description_markup_type', 'administrators', 'display_mode')

class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        exclude = (
                'description_markup_type', 'slug', 
                'administrators', 'display_mode'
            )
