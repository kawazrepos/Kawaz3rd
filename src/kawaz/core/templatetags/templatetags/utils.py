from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, pattern):
    """
    現在のURLのregexを渡して、一致していた場合はstringを返します
    そうでない場合は空白文字を返します
    param request Requestオブジェクト
    param pattern 現在のURLの正規表現パターン
    param string パターンがマッチしたときに返却する文字列

    Example:
        {% load utils %}
        <div class="{% active '/members/.+' 'active' %}"</div>

        例えば、このように記述しておくと、bootstrapのタブなど、「特定のページにいるときだけactiveクラスを不可したい」
        という需要に対応できます

    """
    from re import search
    request = context['request']
    if search(pattern, request.path):
        return 'active'
    return ''

