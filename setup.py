#!/usr/bin/env python
from setuptools import setup

setup(name='Kawaz3',
      version='0.1',
      description='All your game are belongs to us.',
      author='''Sapporo Game Creators' Community Kawaz''',
      author_email='webmaster@kawaz.org',
      test_suite = "runtests.runtests",
      url='http://gitlab.kawaz.org/kawaz/third-impact',
      install_requires = [
        'pillow',
        'Django>=1.6.0',
        'factory_boy>=2.2.1',
        'django-markupfield',
        'honcho'
      ],
)
