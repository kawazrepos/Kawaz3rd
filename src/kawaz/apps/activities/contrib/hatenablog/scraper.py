# coding=utf-8
"""
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
import datetime
import requests
from bs4 import BeautifulSoup
from .conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import HatenablogEntry


# RSS2のpubDateのフォーマット
PUBDATE_FORMAT = '%a, %d %b %Y %H:%M:%S %z'


class HatenablogFeedScraper(object):
    def __init__(self, url=None, verbose=False):
        self.url = url or settings.ACTIVITIES_HATENABLOG_FEED_URL
        self.verbose = verbose

    def fetch(self):
        r = requests.get(self.url)
        r.raise_for_status()

        s = BeautifulSoup(r.text)
        entries = s.find_all('item')
        n = len(entries)
        ncreated = 0
        for i, entry in enumerate(entries):
            url = entry.link.string
            title = entry.title.string

            if self.verbose:
                print("- Fetching entry '{}'... ({}/{})".format(
                    title, i+1, n,
                ))

            pub_date = entry.pubdate.string
            created_at = datetime.datetime.strptime(pub_date,
                                                    PUBDATE_FORMAT)
            thumbnail = self._fetch_entry_thumbnail(entry)
            obj, created = HatenablogEntry.objects.update_or_create(
                url=url,
                defaults=dict(
                    title=title,
                    created_at=created_at,
                    thumbnail=thumbnail),
            )
            if created:
                ncreated += 1
        return ncreated, n - ncreated

    def _fetch_entry_thumbnail(self, entry):
        r = requests.get(entry.link.string)
        r.raise_for_status()
        s = BeautifulSoup(r.text)
        thumbnail_url = None
        for meta in s.find_all('meta'):
            if meta.get('property', None) == 'og:image':
                thumbnail_url = meta.get('content')
        if not thumbnail_url:
            return None
        r = requests.get(thumbnail_url)
        filename = thumbnail_url.split('/')[-1]
        img = SimpleUploadedFile(filename, r.content)
        return img
