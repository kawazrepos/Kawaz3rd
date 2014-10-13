Kawaz3rd
===============================================================
.. image:: https://secure.travis-ci.org/kawazrepos/Kawaz3rd.svg?branch=develop
    :target: http://travis-ci.org/kawazrepos/Kawaz3rd
    :alt: Build status
.. image:: https://coveralls.io/repos/kawazrepos/Kawaz3rd/badge.png?branch=develop
    :target: https://coveralls.io/r/kawazrepos/Kawaz3rd
    :alt: Coverage
.. image:: https://gemnasium.com/kawazrepos/Kawaz3rd.svg
    :target: https://gemnasium.com/kawazrepos/Kawaz3rd
    :alt: Dependency Status

Author
    - Alisue <lambdalisue@hashnote.net>  
    - giginet <giginet.net@gmail.com>
Supported python versions
    Python 3.4
Supported django versions
    Django 1.7

This is a new web site for game creator's community Kawaz_.
It is developed with Python_ 3.4 + Django_ 1.7.

All your games are belong to us.

.. _Kawaz: http://www.kawaz.org/
.. _Python: https://www.python.org/
.. _Django: https://www.djangoproject.com/


Install Kawaz 3rd
---------------------------------------------------------------
Kawaz 3rd is developed in
`github repository <https://github.com/kawazrepos/Kawaz3rd>`_.
Thus you can checkout the repository and install required package with

.. code-block:: sh
    
    $ git clone --recursive https://github.com/kawazrepos/Kawaz3rd
    $ pip install tox
    $ pip install -r config/requirements.txt
    $ pip install -r config/requirements-test.txt

Remember that if you will need to push the changes to the repository_,
You need to use git@github.com:kawazrepos/Kawaz3rd instead.

.. code-block:: sh
    
    $ git clone --recursive git@github.com:kawazrepos/Kawaz3rd
    $ pip install tox
    $ pip install -r config/requirements.txt
    $ pip install -r config/requirements-test.txt

.. _repository: https://github.com/kawazrepos/Kawaz3rd 


Run tests
---------------------------------------------------------------

With clean environment
~~~~~~~~~~~~~~~~~~~~~~
Use tox_ to test Kawaz in clean environment.
You need to run the test in this before pushing the changes to repository.

.. code-block:: sh

    $ tox -c config/tox.ini

It will create newly flesh environment and run the test.

.. _tox: https://tox.readthedocs.org/en/latest/

While development
~~~~~~~~~~~~~~~~~~
You might need to be patient with using tox_ while it will rebuild the environment just before running the test.
To accelerate your development, the following command can be used to run all/specified tests quickly

.. code-block:: sh

    $ python manage.py test kawaz                   # it will test all tests
    $ python manage.py test kawaz.core.personas     # it will test only Personas app

But **please run `tox` at least once before pushing the changes** to prevent local exceptions.


Run development server 
---------------------------------------------------------------
To check the design or client-side codds, you need to run Kawaz in development server.
To do that, type commands below

.. code-block:: sh

    $ python manage.py init_database
    $ python manage.py compilemessages
    $ honcho start -f config/Procfile.dev

It will start development server at localhost:8000 and livereload server at localhost:35217
You can access it with http://localhost:8000/ and if you turn on LiveRelad_ extension of Google Chrome, the changes automatically trigger browser update.

.. _LiveReload: https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei


Run production server
--------------------------------------------------------------
If you are ready to run Kawaz in production server, follow the instruction below.

1.  Write ``src/kawaz/local_settings.py`` to specify the followings

    -   Email addresses of administrators
    -   Cache configurations
    -   Database configurations
    -   Email configurations
    -   SECRET_KEY
    -   Google Calendar ID

    See ``src/kawaz/local_settings.sample.py``

2.  Create a new flesh database or drop all tables in the database
3.  Run ``python manage.py init_database``. You may required to use
    the command with ``--force`` option
4.  Run ``python manage.py compilemessages``
5.  Run ``python manage.py collectstatic``
6.  Configure sever (e.g. apatch) to serve files under 'public'
    directory
7.  Configure server to deploy Kawaz via ``wsgi.py``

