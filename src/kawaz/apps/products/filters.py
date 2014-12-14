from django.db.models import BLANK_CHOICE_DASH, Count
from django.utils.encoding import force_text
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _
import django_filters
from django_filters import filters
from .models import Product
from .models import Category, Platform
from kawaz.core.filters.widgets import ListGroupLinkWidget


class PlatformListGroupLinkWidget(ListGroupLinkWidget):
    """
    プラットフォームアイコンを一覧に出すWidget
    """
    def __init__(self, attrs=None, choices=()):
        super().__init__(attrs, choices)
        # 1度のSQLで全てのプラットフォームが取得できるようにここで予め取得している
        platforms = Platform.objects.all().annotate(products_count=Count('products'))
        self.info = {str(platform.pk): {'url': platform.icon.url, 'count': platform.products_count} for platform in platforms}
        self.all_count = Product.objects.count()

    def render_option(self, name, selected_choices,
                          option_value, option_label):
        """
        各要素のタグを描画している
        BootstrapのListGroupを使用するために以下のようなタグを吐く

        <a class="list-group-item" href="?platform=1"><img class="platform-icon" src="/icon/windows.png">Windows(10)</a>
        """
        option_value = force_text(option_value)
        if option_label == BLANK_CHOICE_DASH[0][1]:
            option_label = _("All")
        data = self.data.copy()
        data[name] = option_value
        selected = data == self.data or option_value in selected_choices

        icon = ''
        count = self.all_count
        if option_value in self.info:
            icon = self.info[option_value]['url']
            count = self.info[option_value]['count']
        try:
            url = data.urlencode()
        except AttributeError:
            url = urlencode(data)
        return self.option_string() % {
            'attrs': selected and ' class="list-group-item active"' or ' class="list-group-item"',
            'query_string': url,
            'label': force_text(option_label),
            'icon': icon,
            'count': count
        }

    def option_string(self):
        return '<a%(attrs)s href="?%(query_string)s"><img class="platform-icon" src="%(icon)s">%(label)s (%(count)s)</a>'


class ProductFilter(django_filters.FilterSet):
    platforms = filters.ModelChoiceFilter(
        label=_('Platforms'),
        queryset=Platform.objects.all(),
        widget=PlatformListGroupLinkWidget(choices=[('', _('All'))]))

    categories = filters.ModelChoiceFilter(
        label=_('Categories'),
        queryset=Category.objects.all(),
        widget=ListGroupLinkWidget(choices=[('', _('All'))]))

    class Meta:
        model = Product
        fields = ['platforms', 'categories',]
