import json
from urllib.request import urlopen, Request
from django.conf import settings
__author__ = 'giginet'

API_URL = 'https://www.googleapis.com/urlshortener/v1/url'

def shorten(url):
    """
    与えられたURLをgoo.glを使って短縮します

    settings.GOOGLE_URL_SHORTENER_API_KEYが設定されているときはそれを使って短縮します。
    詳細は以下を参照してください
    https://developers.google.com/url-shortener/v1/getting_started#auth
    """
    api_key = getattr(settings, 'GOOGLE_URL_SHORTENER_API_KEY', None)
    try:
        api_url = API_URL
        if api_key:
            api_url = '{}?key={}'.format(api_url, api_key)
        data = json.dumps({'longUrl': url})
        data = data.encode('utf-8')
        request = Request(api_url, data)
        request.add_header('Content-Type', 'application/json')
        r = urlopen(request)
        json_string = r.read().decode("utf-8")
        return json.loads(json_string)['id']
    except Exception as e:
        if settings.DEBUG:
            # デバッグ環境においては例外を発生させる
            raise e
        # 本番環境に置いてはfail silently
        return url