import json
import urllib
__author__ = 'giginet'

def shorten(url):
    """
    与えられたURLをgoo.glを使って短縮します
    """
    API_URL = 'https://www.googleapis.com/urlshortener/v1/url'
    try:
        data = json.dumps({'longUrl': url })
        request = urllib.request.Request(API_URL, data)
        request.add_header('Content-Type', 'application/json')
        r = urllib.request.urlopen(request)
        return json.loads(r.read())['id']
    except urllib.error.HTTPError:
        return url
