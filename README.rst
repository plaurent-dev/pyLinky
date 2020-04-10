
pyLinky
=======

.. image:: https://travis-ci.org/Pirionfr/pyLinky.svg?branch=master
    :target: https://travis-ci.org/Pirionfr/pyLinky

.. image:: https://img.shields.io/pypi/v/pyLinky.svg
    :target: https://pypi.python.org/pypi/pyLinky

.. image:: https://img.shields.io/pypi/pyversions/pyLinky.svg
    :target: https://pypi.python.org/pypi/pyLinky

.. image:: https://requires.io/github/Pirionfr/pyLinky/requirements.svg?branch=master
    :target: https://requires.io/github/Pirionfr/pyLinky/requirements/?branch=master
    :alt: Requirements Status

Get your consumption data from your Enedis account (www.enedis.fr) 

This library This is based on jeedom_linky, created by Outadoc (https://github.com/Asdepique777/jeedom_linky)

Installation
------------

The easiest way to install the library is using `pip <https://pip.pypa.io/en/stable/>`_::

    pip install pylinky

You can also download the source code and install it manually::

    cd /path/to/pylinky/
    python setup.py install

    
Note on branch feature/enedis
------------
Ceci un premier jet et nécessite la vision d'un mainteneur du projet.


    from pylinky import LinkyClient
    client = LinkyClient(id, secret, redirect_uri)
    client.login()
    print(client.get_data(scope='IDENTITY'))
    print(client.get_data(scope='DAILY_CONSUMPTION',start_date='2020-04-08',end_date='2020-04-09'))

Usage
-----
Print your current data

    pylinky -u <USERNAME> -p <PASSWORD>

Dev env
-------
create virtual env and install requirements

    virtualenv -p /usr/bin/python3.5 env
    pip install -r requirements.txt

