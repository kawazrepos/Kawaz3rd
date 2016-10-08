# coding=utf-8
"""
"""

import os
from django.conf import settings
from django.core.management.base import BaseCommand
from importlib import import_module
from livereload import Server


class Command(BaseCommand):
    def handle(self, *args, **options):
        server = Server()
        pathlist = []
        # Find statics/templates directories of all installed apps
        for app in settings.INSTALLED_APPS:
            try:
                mod = import_module(app)
            except ImportError as e:
                raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))
            staticfiles_dir = os.path.join(os.path.dirname(mod.__file__),
                                           'statics')
            templates_dir = os.path.join(os.path.dirname(mod.__file__),
                                         'templates')
            if os.path.isdir(staticfiles_dir):
                pathlist.append("{}".format(staticfiles_dir))
            if os.path.isdir(templates_dir):
                pathlist.append("{}".format(templates_dir))
        # STATICFILES_DIRS, TEMPLATE_DIRS
        for path in settings.STATICFILES_DIRS:
            pathlist.append("{}".format(path))
        for path in settings.TEMPLATES[0]['DIRS']:
            pathlist.append("{}".format(path))
        print('Start livereloading with followings...')
        for path in pathlist:
            print('- {}'.format(path))
            server.watch(path)
        # Listen 35729 which is a common port for LiveReload browser ext.
        server.serve(port=35729)
