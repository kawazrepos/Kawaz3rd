Kawaz3rd
===============================================================
.. image:: https://secure.travis-ci.org/kawazrepos/Kawaz3rd.png?branch=develop
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
    Python 3.3
Supported django versions
    Django 1.6

This is a new web site for game creator's community Kawaz_.
It is developed with Python 3.3 + Django 1.6.

All your game are belong to us.

.. _Kawaz: http://www.kawaz.org/

Install Kawaz 3rd
---------------------------------------------------------------
Kawaz 3rd is developed in
`github repository <https://github.com/kawazrepos/third-impact>`_.
Thus you can checkout the repository and install required package with
(You might need to use ``pip3`` instead):

.. code-block:: sh
    
    $ git clone --recursive https://github.com/kawazrepos/Kawaz3rd
    $ pip install -r requirements.txt
    $ pip install -r requirements-test.txt

Remember that if you will need to push the changes to the repository_,
You need to use git@github.com:kawazrepos/third-impact instead.

.. code-block:: sh
    
    $ git clone --recursive git@github.com:kawazrepos/Kawaz3rd
    $ pip install -r requirements.txt

.. _repository: https://github.com/kawazrepos/Kawaz3rd 

.. note::
    Kawaz 3rd does not require to install it on the system.
    So you don't need to run ``python setup.py install`` command like
    previous Kawaz version


Run tests
---------------------------------------------------------------
If you have not install testing package yet, run the following commands to
install required testing packages
(You might need to use ``pip3`` instead):


.. code-block:: sh

    $ pip install tox
    $ pip install -r requirements-test.txt

You can quickly test Kawaz 3rd in current environment with the following
commands
(You might need to use ``python3`` instead):

.. code-block:: sh

    $ python runtests.py

Or you can test Kawaz 3rd in clean environment with the following commands.

.. code-block:: sh

    $ tox


Run development server 
---------------------------------------------------------------
If you have not create the database yet, run the following commands to create
the database. It is also required when new apps is added
(You might need to use ``python3`` instead):

.. code-block:: sh

    $ python manage.py syncdb

Then you can start the development server with:

.. code-block:: sh

    $ honcho start -f Procfile.dev

It will start development server at localhost:8000.
You can access it with http://localhost:8000/
