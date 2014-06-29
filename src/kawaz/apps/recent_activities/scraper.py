#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/29
#
from lxml import etree
from PIL import Image
import os
import io
import urllib
import datetime
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from .models import RecentActivity

__author__ = 'giginet'


FEED_URL = settings.RECENT_ACTIVITY_FEED_URL
# RSS2のpubDateのフォーマット
PUBDATE_FORMAT = '%a, %d %b %Y %H:%M:%S %z'

class RecentActivityScraper(object):
    def __init__(self):
        pass

    def fetch(self):
        feed = urllib.request.urlopen(FEED_URL).read()
        root = etree.fromstring(feed, etree.XMLParser())
        items = [elem for elem in root.iter('item')]
        for item in items:
            title = item.find('title').text
            link = item.find('link').text
            print('Fetching entry {}'.format(title))
            pub_date = item.find('pubDate').text
            publish_at = datetime.datetime.strptime(pub_date, PUBDATE_FORMAT)
            image_url = self._fetch_thumbnail(link)
            filename = os.path.basename(image_url)
            image_data = urllib.request.urlopen(image_url).read()
            image = SimpleUploadedFile(filename, image_data)
            try:
                RecentActivity.objects.get(url=link)
            except:
                RecentActivity.objects.create(title=title,
                                              url=link,
                                              publish_at=publish_at,
                                              thumbnail=image)

    def _fetch_thumbnail(self, link):
        """
        はてなブログのエントリURLからサムネイルURLを取り出します
        サムネイルはFeedには埋まってなくて、各ページのOpen Graph Protocolとして埋まっているので
        ページごとにfetchします
        """
        entry = urllib.request.urlopen(link).read()
        root = etree.fromstring(entry, etree.HTMLParser())
        head = root.find('head')
        for meta in head.findall('meta'):
            property = meta.attrib.get('property', None)
            if property == 'og:image':
                return meta.attrib['content']
