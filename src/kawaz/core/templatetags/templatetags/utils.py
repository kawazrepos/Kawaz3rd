from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, pattern):
    """
    現在のURLのregexを渡して、一致していた場合は'active'を返します
    そうでない場合は空白文字を返します
    param pattern 現在のURLの正規表現パターン

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

