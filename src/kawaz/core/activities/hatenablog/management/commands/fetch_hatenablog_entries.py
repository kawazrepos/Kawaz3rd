from optparse import make_option
from django.core.management.base import NoArgsCommand
from ...conf import settings
from ...models import HatenablogEntry
from ...scraper import HatenablogFeedScraper

URL = settings.ACTIVITIES_HATENABLOG_FEED_URL


class Command(NoArgsCommand):
    help = ("Command to fetch entries in Hatenablog. "
            "It will ignore duplicated entries.")

    option_list = NoArgsCommand.option_list + (
        make_option('--clear', action='store_true', default=False,
                    help=("Clear entries in database to synchronize "
                          "entries in database and actual.")),
        make_option('--url',
                    default=settings.ACTIVITIES_HATENABLOG_FEED_URL,
                    help=("Specify a url of hatenablog which will be parsed. "
                          "The default url is '{}'.").format(URL)),
    )

    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity'))
        if options.get('clear'):
            if verbosity > 0:
                print(("Clearing hatenablog entries in database..."))
            HatenablogEntry.objects.clear()

        if verbosity > 0:
            print(("Fetching hatenablog entries from '{}'...").format(
                options.get('url'),
            ))
        scraper = HatenablogFeedScraper(url=options.get('url'),
                                        verbose=verbosity > 0)
        ncreated, nupdated = scraper.fetch()

        if verbosity > 0:
            print("*" * 80 + "\n")
            print(("{} hatenablog entries are created.\n"
                "{} hatenablog entries are updated.\n").format(ncreated, nupdated))
            print("*" * 80)
