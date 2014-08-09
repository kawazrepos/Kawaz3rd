from urllib.parse import urlencode
from django_filters.widgets import LinkWidget
from django.forms.widgets import flatatt
from django.db.models.fields import BLANK_CHOICE_DASH
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _

__author__ = 'giginet'


class ListGroupLinkWidget(LinkWidget):
    """
    Django FilterのfieldsをBootstrapのList Groupを使って出力するWidget

    <div class="list-group">
        <a href="list-group-item" class="">All</a>
        <a href="list-group-item active" class="">Item1</a>
        <a href="list-group-item" class="">Item2</a>
    </div>
    """

    def render(self, name, value, attrs=None, choices=()):
        if not hasattr(self, 'data'):
            self.data = {}
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs)
        output = ['<div class="list-group"%s>' % flatatt(final_attrs)]
        options = self.render_options(choices, [value], name)
        if options:
            output.append(options)
        output.append('</div>')
        return mark_safe('\n'.join(output))

    def render_option(self, name, selected_choices,
                      option_value, option_label):
        option_value = force_text(option_value)
        if option_label == BLANK_CHOICE_DASH[0][1]:
            option_label = _("All")
        data = self.data.copy()
        data[name] = option_value
        selected = data == self.data or option_value in selected_choices
        try:
            url = data.urlencode()
        except AttributeError:
            url = urlencode(data)
        return self.option_string() % {
             'attrs': selected and ' class="list-group-item active"' or '',
             'query_string': url,
             'label': force_text(option_label)
        }

    def option_string(self):
        return '<a%(attrs)s href="?%(query_string)s" class="list-group-item">%(label)s</a>'
