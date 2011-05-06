=========================
 README: NSMemcached 0.1
=========================

:Author: Nicolas Perriault
:Contact: np@akei.com

.. contents::

Abstract
========

NSMemcached is simple yet efficient Python implementation of a
`namespaced client`_ for memcached_ on top of the python-memcached_ package.

Quick Start
===========

Sample usage:

    >>> import memcache
    >>> from nsmemcached.client import NamespacedClient
    >>> std_client = memcache.Client(['127.0.0.1:11211'])
    >>> ns_client = NamespacedClient(std_client)
    >>> ns_client.set('foo', 'bar', ns='barspace')
    True
    >>> ns_client.get('foo', ns='barspace')
    bar
    >>> ns_client.get('foo')
    None
    >>> ns_client.clear_ns('barspace')
    >>> ns_client.get('foo', ns='barspace')
    None

Yes, that simple.

Caveats
=======

Namespace keys are stored in dedicated keys, so every time you request a
namespaced item you'll make two queries to the memcached server instead of one,
so expect a tiny slowdown compared to the standard way of using the standard,
non-namespaced memcached API.

Dependencies and Compatibility
==============================

NSMemcached requires the use of Python 2.4 or more recent.

Installing python-memcached_ package is required in order to use this library,
as well as a working memcached_ server instance, obviously.

NSMemcached is fully compatible with the API of the standard python-memcached_
client.

License
=======

This code is released under the terms of the `MIT License`_.

Author
======

Nicolas Perriault, AKEI_, ``<np at akei dot com>``

.. _namespaced client: http://code.google.com/p/memcached/wiki/FAQ#Deleting_by_Namespace
.. _memcached: http://memcached.org/
.. _python-memcached: http://pypi.python.org/pypi/python-memcached/
.. _MIT License: http://en.wikipedia.org/wiki/MIT_License
.. _AKEI: http://akei.com/
