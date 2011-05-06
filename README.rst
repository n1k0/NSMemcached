===========================
 README: NSMemcached 0.2.1
===========================

:Author: Nicolas Perriault
:Contact: np at akei com

.. contents::

Abstract
========

NSMemcached_ is simple yet efficient Python implementation of a
`namespaced client`_ for memcached_ on top of the python-memcached_ package.

Quick Start
===========

Sample usage:

    >>> from nsmemcached import Client
    >>> ns_client = Client(['127.0.0.1:11211'])
    >>> ns_client.set('foo', 'bar', ns='barspace')
    True
    >>> ns_client.set('zoo', 'baz', ns='barspace')
    True
    >>> ns_client.get('foo', ns='barspace')
    'bar'
    >>> ns_client.get('zoo', ns='barspace')
    'baz'
    >>> ns_client.get('foo')
    >>> ns_client.get('zoo')
    >>> ns_client.clear_ns('barspace')
    True
    >>> ns_client.get('foo', ns='barspace')
    >>> ns_client.get('zoo', ns='barspace')

Yes, that simple. Other python-memcached_ client methods are supported as well,
sharing the same signature but with a supplementary ``ns`` named argument
available to optionaly declare a namespace to perform the query within::

    >>> ns_client.set('foo', 1, ns='bar')
    True
    >>> ns_client.incr('foo', ns='bar')
    2
    >>> ns_client.decr('foo', ns='bar')
    1
    >>> ns_client.set('foo', 'bar, ns='bar')
    True
    >>> ns_client.append('foo', '!!!', ns='bar')
    True
    >>> ns_client.get('foo', ns='bar')
    'bar!!!'
    >>> ns_client.delete('foo', ns='bar')
    True
    >>> ns_client.get('foo', ns='bar')

The best way to learn about the usage of all the available methods from the API
is probably to dig into the `test suite code`_ which covers 100% of them.

Caveats
=======

Namespace keys are stored in dedicated keys, so every time you request a
namespaced item you'll make two queries to the memcached server instead of one,
so expect a tiny slowdown compared to the way of using the standard,
non-namespaced `memcached API`_.

Also, python-memcached_ client's ``get_multi()`` and ``set_multi()`` are not
currently supported (yet).

Dependencies and Compatibility
==============================

NSMemcached_ requires the use of Python 2.4 or more recent.

Installing python-memcached_ package is required in order to use this library,
as well as a working memcached_ server instance, obviously.

NSMemcached_ is fully compatible with the API of the standard python-memcached_
client.

License
=======

This code is released under the terms of the `MIT License`_.

Author
======

Nicolas Perriault, AKEI_, ``<np at akei com>``

.. _namespaced client: http://code.google.com/p/memcached/wiki/FAQ#Deleting_by_Namespace
.. _memcached: http://memcached.org/
.. _memcached API: http://code.google.com/p/memcached/wiki/NewCommands
.. _NSMemcached: http://pypi.python.org/pypi/NSMemcached
.. _python-memcached: http://pypi.python.org/pypi/python-memcached/
.. _test suite code: https://github.com/n1k0/NSMemcached/blob/master/nsmemcached/tests.py
.. _MIT License: http://en.wikipedia.org/wiki/MIT_License
.. _AKEI: http://akei.com/
