# -*- coding: utf-8 -*-

import memcache
import unittest

from client import NamespacedClient


class CacheTest(unittest.TestCase):
    def test_namespaces(self):
        std_client = memcache.Client(['127.0.0.1:11211'], debug=0)
        if len(std_client.get_stats()) < 1:
            raise RuntimeError('memcached server down, cannot run tests')
        self.assertRaises(ValueError, NamespacedClient, 'plop')
        nsclient = NamespacedClient(std_client)
        nsclient.flush_all()
        self.assertEquals(nsclient.get('blah'), None)
        nsclient.set('blah', 2)
        self.assertEquals(nsclient.get('blah'), 2)
        self.assertEquals(nsclient.get('blah', ns='foo'), None)
        nsclient.set('blah', 8, ns='foo')
        nsclient.set('blah', 12, ns='bar')
        self.assertEquals(nsclient.get('blah', ns='foo'), 8)
        self.assertEquals(nsclient.get('blah', ns='bar'), 12)
        self.assertEquals(nsclient.get('blah'), 2)
        # namespace clear
        nsclient.clear_ns('foo')
        self.assertEquals(nsclient.get('blah', ns='foo'), None)
        self.assertEquals(nsclient.get('blah', ns='bar'), 12)
        self.assertEquals(nsclient.get('blah'), 2)
        # namespaced key deletion
        nsclient.delete('blah', ns='bar')
        self.assertEquals(nsclient.delete('blah', ns='bar'), None)

if __name__ == '__main__':
    unittest.main()
