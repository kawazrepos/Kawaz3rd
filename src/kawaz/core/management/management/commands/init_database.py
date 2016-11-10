# coding=utf-8
"""
Kawaz開発用にデータベースの初期化等を行うコマンド
"""

import os
import sys
from django.conf import settings
from django.db import DEFAULT_DB_ALIAS
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ("Command to initialize database. "
            "It will overwrite the existing data in database thus "
            "Run this command WITH CLOSE ATTENTION.")

    def add_arguments(self, parser):
        parser.add_argument('--database', default=DEFAULT_DB_ALIAS,
                            help=("Nominates a database to initialize. "
                                  "Defaults to the '{}' database.").format(
                                    DEFAULT_DB_ALIAS))
        parser.add_argument('--noinput', dest='interactive',
                            action='store_false', default=True,
                            help=("Tells Django to NOT prompt the user "
                                  "for input of any kind."))
        parser.add_argument('--force', action='store_true', default=False,
                            help=("Tells Django to run the command even if "
                                  "'settings.DEBUG = False'."))
        parser.add_argument('--no-production-data', dest='load_production_data',
                            action='store_false', default=True,
                            help=("Tells Django to NOT load production data which is "
                                  "also used in production."))
        parser.add_argument('--no-debug-data', dest='load_debug_data',
                            action='store_false', default=True,
                            help=("Tells Django to NOT load debug data which is "
                                  "only used in development."))
        parser.add_argument('--no-fetch-entries', dest='fetch_entries', default=True, action='store_false',
                            help='Tells Django to NOT fetch blog entries from Hatena blog')

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity'))
        options['verbosity'] = verbosity
        database = options.get('database')
        interactive = options.get('interactive')
        force = options.get('force')
        fetch_entries = options.get('fetch_entries')
        
        # The command required to be run in development mode
        if not force and not settings.DEBUG:
            print(("Running this command with 'settings.DEBUG = False' is "
                   "not permitted to prevent unwilling database overwritten. "
                   "Use '--force' option to run the command forcely."),
                  file=sys.stderr)
            sys.exit(1)

        # check the database setting
        DATABASE = settings.DATABASES.get(database)
        engine = DATABASE['ENGINE']
        filename = DATABASE['NAME']
        is_sqlite3 = engine == 'django.db.backends.sqlite3'

        if interactive:
            confirm = input((
                "You have requested to run database initialization. "
                "This will IRREVERSIBLY DESTROY all data current in the "
                "'{}' database, and return each table with initial data. "
                "Are you sure to continue? [y/N]: "
            ).format(filename))
        else:
            confirm = 'yes'
        if confirm not in ('y', 'yes', 'Yes', 'YES'):
            print(("Operation has canceled by user"))
            sys.exit(1)


        # Warn user if the database is not SQLite3 while table dropping is not
        # supported for other databases
        if not is_sqlite3:
            if interactive:
                confirm = input((
                    "You are running this command with non SQLite3 database. "
                    "Making flesh database is only supported for SQLite3 thus "
                    "you may need to drop all your tables manually before "
                    "running this command.\n"
                    "Are you sure to continue? [y/N]: "
                ))
            else:
                confirm = 'yes'
            if confirm not in ('y', 'yes', 'Yes', 'YES'):
                print(("Operation has canceled by user"))
                sys.exit(1)

        else:
            # check if the SQLite3 file exist
            if os.path.exists(filename):
                if interactive:
                    confirm = input((
                        "A database file '{}' is found. "
                        "Do you want to remove this file to make a flesh "
                        "database? [y/N]: ").format(filename)
                    )
                else:
                    confirm = 'yes'
                if confirm in ('y', 'yes', 'Yes', 'YES'):
                    os.remove(filename)

        # call migrate command
        call_command('migrate', **options)

        # load fixtures
        if options.get('load_production_data'):
            call_command('loaddata', 'production', **options)
        if options.get('load_debug_data'):
            call_command('loaddata', 'debug', **options)

        # fetch Hatenablog updates
        if fetch_entries:
            call_command('fetch_hatenablog_entries', **options)

        if verbosity > 0:
            print("*" * 80 + "\n")
            print("The database get ready.")
            print(("Start the development server with honcho as\n\n"
                   "    honcho start -f config/Profile.dev\n\n"
                   "And access to 'http://localhost:8000'"))
            print(("You can login as administrator with:\n\n"
                   "    Username: system\n"
                   "    Password: password\n"))
            print("*" * 80)
