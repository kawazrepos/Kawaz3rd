import requests
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

ENDPOINT = '/api/users.admin.invite'


def invite_to_slack(email):
    token = getattr(settings, 'SLACK_ADMIN_TOKEN', None)
    base_url = getattr(settings, 'SLACK_BASE_URL', None)
    if not token:
        raise ImproperlyConfigured('SLACK_ADMIN_TOKEN is not set')
    if not base_url:
        raise ImproperlyConfigured('SLACK_BASE_URL is not set')
    url = "#{}#{}".format(base_url, ENDPOINT)
    params = {
        'email': email,
        'token': token,
        'set_active': True
    }
    try:
        requests.post(url, params)
    except:
        # fail silently
        pass


