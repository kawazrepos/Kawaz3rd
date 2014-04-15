Kawaz 3rd
===============================================================

.. image:: https://secure.travis-ci.org/kawazrepos/third-impact.png
    :target: http://travis-ci.org/kawazrepos/third-impact
    :alt: Build status

All your game are belong to us.

Setup for Development
---------------------------------------------------------------

.. code-block:: sh

    $ pip install -r requirements.txt
    $ pip install -r requirements-test.txt
    $ python manage.py syncdb
    $ honcho start -f Procfile.dev
