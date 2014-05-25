from django.db import models
from django.utils.translation import ugettext as _
from registration.supplements import RegistrationSupplementBase

class KawazRegistrationSupplement(RegistrationSupplementBase):

    place = models.CharField(_("Place"), max_length=64,
                             help_text=_("Fill your address. You must be related with Sapporo or neighbor cities."))
    skill = models.TextField(_("Skill"), max_length=2048,
                             help_text=_("Fill your skills or what you want to do which related to game development."))
    remarks = models.TextField(_("Remarks"), blank=True)

    def __str__(self):
        # a summary of this supplement
        user = self.registration_profile.user
        return user.username