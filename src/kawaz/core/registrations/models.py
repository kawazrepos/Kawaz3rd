from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from registration.supplements import RegistrationSupplementBase
from registration.models import RegistrationProfile
from registration.signals import user_activated


class RegistrationSupplement(RegistrationSupplementBase):
    """
    新規会員登録時の追加情報
    """
    place = models.CharField(_("Place"), max_length=64, help_text=_(
        "Fill your address. "
        "You must be related with Sapporo or neighbor cities."
    ))
    skill = models.TextField(_("Skill"), max_length=2048, help_text=_(
        "Fill your skills or what you want to do which related to "
        "game development."
    ))
    remarks = models.TextField(_("Remarks"), blank=True, null=True)

    def __str__(self):
        user = self.registration_profile.user
        return user.username


@receiver(user_activated)
def setup_for_participation(sender, user, **kwargs):
    """
    会員登録からアクティベートされたユーザーをChildrenに変更
    """
    user.role = 'children'
    user.save()


# パーミッション関係を設定
from permission import add_permission_logic
from .perms import RegistrationProfilePermissionLogic
add_permission_logic(RegistrationProfile, RegistrationProfilePermissionLogic())


