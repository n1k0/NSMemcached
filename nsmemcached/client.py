# -*- coding: utf-8 -*-

import memcache
import random

MAX_KEY = 1000000


class NamespacedClient(object):
    """ An implementation of namespaces using Memcache.
        See: http://code.google.com/p/memcached/wiki/FAQ#Deleting_by_Namespace

        Sample usage::
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
    """
    mc = None

    def __init__(self, mc):
        """ Constructor, accepting a ``memcache.Client`` instance as first arg.
        """
        if not isinstance(mc, memcache.Client):
            raise ValueError('mc must be an instance of memcache.Client')
        self.mc = mc

    def __getattr__(self, name):
        """ If unknown attribute, fallbacks to the memcache standard client
            instance one.
        """
        return getattr(self.mc, name)

    def add(self, key, val, time=0, min_compress_len=0, ns=None):
        """ Stores a value in an optionaly namespaced key.
        """
        return self.mc.add(self._compute_key(key, ns), val, time=time,
            min_compress_len=min_compress_len)

    def append(self, key, val, time=0, min_compress_len=0, ns=None):
        """ Appends the value to the end of the existing optinaly namespaced
            key's value.
        """
        return self.mc.append(self._compute_key(key, ns), val, time=time,
            min_compress_len=min_compress_len)

    def cas(self, key, val, time=0, min_compress_len=0, ns=None):
        """ Sets an optionaly namespaced key to a given value in the memcache
            if it hasn't been altered since last fetched.
        """
        return self.mc.cas(self._compute_key(key, ns), val, time=time,
            min_compress_len=min_compress_len)

    def clear_ns(self, ns):
        """ Cleans all cached values for all keys within the given namespace.
        """
        self.mc.incr(self._compute_ns_key(ns))

    def decr(self, key, delta=1, ns=None):
        """ Decrements a value stored in an optionaly namspaced key.
        """
        return self.mc.decr(self._compute_key(key, ns), delta=delta)

    def delete(self, key, ns=None, time=0):
        """ Deletes a cached value by its key and an optional namespace.
        """
        return self.mc.delete(self._compute_key(key, ns), time=time)

    def get(self, key, ns=None):
        """ Retrieve a stored value by its key, optionnaly within a given
            namespace.
        """
        return self.mc.get(self._compute_key(key, ns))

    def gets(self, key, ns=None):
        """ Retrieves a value stored in an optionaly namespaced key.
        """
        return self.mc.gets(self._compute_key(key, ns))

    def get_ns_key(self, ns):
        """ Retrieves the stored namespace key name, creates it if it doesn't
            exist.
        """
        ns_key = self.mc.get(self._compute_ns_key(ns))
        if not ns_key:
            ns_key = random.randint(1, MAX_KEY)
            self.mc.set(self._compute_ns_key(ns), ns_key)
        return ns_key

    def incr(self, key, delta=1, ns=None):
        """ Increments a value stored in an optionaly namspaced key.
        """
        return self.mc.incr(self._compute_key(key, ns), delta=delta)

    def prepend(self, key, val, time=0, min_compress_len=0, ns=None):
        """ Prepends the value at the beginning of the existing optinaly
            namespaced key's value.
        """
        return self.mc.prepend(self._compute_key(key, ns), val, time=time,
            min_compress_len=min_compress_len)

    def replace(self, key, val, time=0, min_compress_len=0, ns=None):
        """ Replaces existing optoinaly namespaced key with value.
        """
        return self.mc.replace(self._compute_key(key, ns), val, time=time,
            min_compress_len=min_compress_len)

    def set(self, key, val, ns=None, **kwargs):
        """ Stores a values with given key, optionnaly within a given
            namespace.
        """
        return self.mc.set(self._compute_key(key, ns), val, **kwargs)

    def _compute_key(self, key, ns=None):
        """ Computes key name, depending if it's tied to a namespace.
        """
        if not isinstance(key, basestring):
            raise NotImplementedError('nsmemcached only handles string keys')
        if ns:
            key = '%s_%d_%s' % (ns, self.get_ns_key(ns), str(key),)
        return str(key)

    def _compute_ns_key(self, ns):
        """ Computes a namespace key name.
        """
        if not isinstance(ns, basestring):
            raise NotImplementedError('nsmemcached only handles string ns')
        return str('%s_ns_key' % ns)
