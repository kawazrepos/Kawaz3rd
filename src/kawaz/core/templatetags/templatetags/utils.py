from django import template
from django.contrib.sites.models import Site

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, pattern):
    """
    現在のURLのregexを渡して、一致していた場合は'active'を返します
    そうでない場合は空白文字を返します
    param pattern 現在のURLの正規表現パターン

    また、GETパラメーターが与えられている場合、keyの昇順に連結されたURLで判定します
    /members/kawaz_tan/?a=1&b=2&c=3

    Example:
        {% load utils %}
        <div class="{% active '/members/.+' %}"</div>

        例えば、このように記述しておくと、bootstrapのタブなど、「特定のページにいるときだけactiveクラスを付加したい」
        という需要に対応できます

    """
    from re import search
    request = context['request']
    if list(request.GET):
        url = '{}?{}'.format(request.path, request.GET.urlencode())
    else:
        url = request.path
    if search(pattern, url):
        return 'active'
    return ''



@register.simple_tag()
def get_week_day(date):
    """
    datetimeオブジェクトを受け取り、曜日に応じてCSSクラス名を返します

    Param
        date [datetime]

    Return [string]
        土曜日 saturday
        日曜日 sunday
        その他 weekday

    Example
        {% load utils %}
        <div class="{% get_week_day date">{{ date }}</div>

    """
    wd = date.weekday()
    if wd == 5:
        return "saturday"
    elif wd == 6:
        return "sunday"
    return "weekday"


@register.assignment_tag
def get_current_site():
    """
    現在のSiteオブジェクトを取得します
    """
    return Site.objects.get_current()
