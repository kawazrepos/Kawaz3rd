# coding=utf-8
import sys
from setuptools import setup, find_packages

NAME = 'Kawaz3'
VERSION = '0.1.0'

def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()

def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)

setup(
    name = NAME,
    version = VERSION,
    description = "A portal website of Sapporo Game Creators' Community Kawaz",
    long_description = read('README.rst'),
    classifiers = (
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet :: WWW/HTTP',
    ),
    keywords = "django Kawaz",
    author = 'Kawaz',
    author_email = 'webmaster@kawaz.org',
    url = 'https://github.com/kawazrepos/%s' % NAME,
    download_url = 'https://github.com/kawazrepos/%s/tarball/master' % NAME,
    license = 'MIT',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data = True,
    package_data = {
        '': ['README.rst',
             'requirements.txt',
             'requirements-test.txt',
             'requirements-docs.txt'],
    },
    zip_safe=True,
    install_requires=readlist('requirements.txt'),
    test_suite="runtests.runtests",
    tests_require=readlist('requirements-test.txt'),
)
