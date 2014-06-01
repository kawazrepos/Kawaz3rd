from django.db import models
from django.utils.translation import ugettext as _
from registration.supplements import RegistrationSupplementBase
from registration.models import RegistrationProfile


class RegistrationSupplement(RegistrationSupplementBase):

    place = models.CharField(
        _("Place"), max_length=64,
        help_text=_("Fill your address. You must be related with Sapporo or "
                    "neighbor cities."))
    skill = models.TextField(
        _("Skill"), max_length=2048,
        help_text=_("Fill your skills or what you want to do which related to "
                    "game development."))
    remarks = models.TextField(_("Remarks"), blank=True, null=True)

    def __str__(self):
        user = self.registration_profile.user
        return user.username

from permission import add_permission_logic
from .perms import RegistrationProfilePermissionLogic
add_permission_logic(RegistrationProfile, RegistrationProfilePermissionLogic())


from django.dispatch import receiver
from registration.signals import user_activated


@receiver(user_activated)
def add_role_to_new_user(user, password, is_generated, request, **kwargs):
    user.role = 'children'      # ユーザーをChildrenにする
    user.save()
