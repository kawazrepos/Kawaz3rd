# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

#if not hasattr(settings, "JQUERY_PATH"):
#    raise ImproperlyConfigured("You must define the JQUERY_PATH setting before using the field.")

# jQuery MarkItUp
settings.MARKITUP_PATH          = getattr(settings, 'MARKITUP_PATH', 'javascript/markitup')
_PATH = lambda x: "%s/%s"%(settings.MARKITUP_PATH, x)
settings.MARKITUP_SET           = getattr(settings, 'MARKITUP_SET', _PATH('sets/default'))
settings.MARKITUP_SKIN          = getattr(settings, 'MARKITUP_SKIN',_PATH('skins/markitup'))
settings.MARKITUP_SCRIPT_PATH   = getattr(settings, 'MARKITUP_SCRIPT_PATH', _PATH('jquery.markitup.js'))

settings.MARKITUPFIELD_SCRIPT_PATH = getattr(settings, 'MARKITUPFIELD_SCRIPT_PATH', 'javascript/jquery.django-markitupfield.js')