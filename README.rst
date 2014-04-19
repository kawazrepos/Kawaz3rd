Kawaz 3rd
===============================================================
.. image:: https://secure.travis-ci.org/kawazrepos/third-impact.png
    :target: http://travis-ci.org/kawazrepos/third-impact
    :alt: Build status
.. image:: https://coveralls.io/repos/kawazrepos/third-impact/badge.png
    :target: https://coveralls.io/r/kawazrepos/third-impact/
    :alt: Coverage

Author
    Alisue <lambdalisue@hashnote.net>
    Giginet
Supported python versions
    Python 3.3
Supported django versions
    Django 1.6

This is a new web site for game creator's community Kawaz_.
It is developed with Python 3.3 + Django 1.6.

.. _Kawaz: http://www.kawaz.org/

Install Kawaz 3rd
---------------------------------------------------------------
Kawaz 3rd is developed in
`github repository <https://github.com/kawazrepos/third-impact>`_.
Thus you can checkout the repository and install required package with
(You might need to use ``pip3`` instead):

.. code-block:: sh
    
    $ git clone https://github.com/kawazrepos/third-impact
    $ pip install -r requirements.txt
    $ pip install -r requirements-test.txt

Remember that if you will need to push the changes to the repository_,
You need to use `git@github.com:kawazrepos/third-impact`_ instead.

.. code-block:: sh
    
    $ git clone git@github.com:kawazrepos/third-impact
    $ pip install -r requirements.txt

.. _repository: https://github.com/kawazrepos/third-impact 

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
