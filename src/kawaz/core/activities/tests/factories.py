# ! -*- coding: utf-8 -*-
#
# created by giginet on 2014/10/15
#
import datetime
from django.utils import timezone

import factory
from kawaz.core.personas.tests.factories import PersonaFactory
from activities.models import Activity



class ActivityFactory(factory.DjangoModelFactory):

    class Meta:
        model = Activity
