#!/usr/bin/env python
from setuptools import setup

setup(name='Kawaz',
      version='0.1',
      description='All your game are belongs to us.',
      author='Kawaz',
      author_email='webmaster@kawaz.org',
      url='https://gitlab.kawaz.org/kawaz/third-impact',
      install_requires = [
        'Django>=1.6.0',
        'factory_boy>=2.2.1',
        'django-markupfield',
        'honcho'
      ],
)