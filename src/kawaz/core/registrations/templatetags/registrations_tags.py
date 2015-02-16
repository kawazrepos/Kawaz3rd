from django import template
from django.template import TemplateSyntaxError
from registration.models import RegistrationProfile

register = template.Library()

@register.assignment_tag(takes_context=True)
def get_registration_profiles(context, status=None):
    """
    渡されたステータスのRegistrationProfileを取り出すテンプレートタグ
    ただし、registration.activate_userを持たないユーザーが呼び出しても何も取り出せない。
    何も引数を渡さないとき、全てのRegistrationProfileを取り出せる

    Status:
        untreated : 未処理
        accepted : 承認済み
        rejected : 否認済み

    Example:
        {% load registrations_tags %}
        {% get_registration_profile untreated as profiles %}
    """
    user = context.get('user', None)
    profiles = RegistrationProfile.objects.all()
    if status in ['untreated', 'accepted', 'rejected']:
        # ステータスが正常なとき、フィルターする
        profiles = profiles.filter(_status=status)
    elif status:
        # ステータスが設定されていて、不正なとき、例外を投げる
        raise TemplateSyntaxError("""'status' argument must be untreated, accepted or rejected.""")
    if not user.has_perm('registration.activate_user'):
        # パーミッションがなければNoneを返す
        return None
    return profiles
