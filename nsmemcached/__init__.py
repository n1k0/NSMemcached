# -*- coding: utf-8 -*-

import memcache

from client import NamespacedClient

VERSION = (0, 2, 1)
__version__ = '.'.join([str(x) for x in VERSION])


class Client(NamespacedClient):
    """ Just a convenient Client class to ease import and instantiation::

        >>> from nsmemcached import Client
        >>> ns_client = Client(['127.0.0.1:11211'])
    """
    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(memcache.Client(*args, **kwargs))
