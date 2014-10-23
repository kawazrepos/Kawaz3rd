from django import forms
from django.forms import ModelForm, ModelChoiceField
from kawaz.core.forms.fields import MarkdownField
from django.utils.translation import ugettext as _
from kawaz.core.forms.mixins import Bootstrap3HorizontalFormHelperMixin
from .models import Category

from .models import Entry

class CategoryChoiceField(ModelChoiceField):
    """
    ModelChoiceFieldのラベルにCategory.labelが使われるようにする
    """

    def label_from_instance(self, obj):
        return obj.label

class EntryForm(Bootstrap3HorizontalFormHelperMixin, ModelForm):

    body = MarkdownField(label=_('Body'))
    category = CategoryChoiceField(queryset=Category.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(author=user)

    class Meta:
        model = Entry
        exclude = (
            'author',
            'created_at',
            'updated_at',
            'publish_at',
        )
