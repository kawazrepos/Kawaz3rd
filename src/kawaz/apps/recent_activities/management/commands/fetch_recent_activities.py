#! -*- coding: utf-8 -*-
#
# created by giginet on 2014/6/29
#
__author__ = 'giginet'

from django.core.management.base import BaseCommand, CommandError
from ...scraper import RecentActivityScraper

class Command(BaseCommand):
    def handle(self, *args, **options):
        scraper = RecentActivityScraper()
        scraper.fetch()
