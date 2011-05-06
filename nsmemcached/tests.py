# -*- coding: utf-8 -*-

import unittest

from __init__ import Client


class CacheTest(unittest.TestCase):
    client = None

    def setUp(self):
        self.client = Client(['127.0.0.1:11211'], debug=1)
        if len(self.client.get_stats()) < 1:
            raise RuntimeError('memcached server seems down, cannot run tests')

    def test_add(self):
        self.client.flush_all()
        self.assertEquals(self.client.add('foo', 'plop', ns='bar'), True)
        self.assertEquals(self.client.get('foo'), None)
        self.assertEquals(self.client.get('foo', ns='bar'), 'plop')
        # namespace clear
        self.client.clear_ns('bar')
        self.assertEquals(self.client.get('foo', ns='bar'), None)

    def test_append_prepend(self):
        self.client.flush_all()
        self.client.add('foo', 'plop', ns='bar')
        self.assertEquals(self.client.append('foo', '!!!', ns='bar'), True)
        self.assertEquals(self.client.get('foo', ns='bar'), 'plop!!!')
        self.assertEquals(self.client.prepend('foo', '!!!', ns='bar'), True)
        self.assertEquals(self.client.get('foo', ns='bar'), '!!!plop!!!')

    def test_cas(self):
        self.client.flush_all()
        self.client.add('foo', 'plop', ns='bar')
        self.client.get('foo', ns='bar')
        self.assertEquals(self.client.cas('foo', 'baz', ns='bar'), True)
        self.assertEquals(self.client.get('foo', ns='bar'), 'baz')

    def test_get_set_gets_delete_clear(self):
        self.client.flush_all()
        self.assertEquals(self.client.get('blah'), None)
        self.client.set('blah', 2)
        self.assertEquals(self.client.get('blah'), 2)
        self.assertEquals(self.client.get('blah', ns='foo'), None)
        self.client.set('blah', 8, ns='foo')
        self.client.set('blah', 12, ns='bar')
        self.assertEquals(self.client.get('blah', ns='foo'), 8)
        self.assertEquals(self.client.get('blah', ns='bar'), 12)
        self.assertEquals(self.client.get('blah'), 2)
        # namespace clear
        self.client.clear_ns('foo')
        self.assertEquals(self.client.get('blah', ns='foo'), None)
        self.assertEquals(self.client.get('blah', ns='bar'), 12)
        self.assertEquals(self.client.get('blah'), 2)
        # namespaced key deletion
        self.client.delete('blah', ns='bar')
        self.assertEquals(self.client.get('blah', ns='bar'), None)
        # gets
        self.client.set('foo', 2, ns='bar')
        self.assertEquals(self.client.gets('foo', ns='bar'), 2)

    def test_incr_decr(self):
        self.client.flush_all()
        self.client.set('foo', 1)
        self.client.set('foo', 10, ns='bar')
        self.assertEquals(self.client.incr('foo'), 2)
        self.assertEquals(self.client.get('foo'), 2)
        self.assertEquals(self.client.incr('foo', ns='bar'), 11)
        self.assertEquals(self.client.get('foo', ns='bar'), 11)
        self.assertEquals(self.client.decr('foo'), 1)
        self.assertEquals(self.client.get('foo'), 1)
        self.assertEquals(self.client.decr('foo', ns='bar'), 10)
        self.assertEquals(self.client.get('foo', ns='bar'), 10)
        # namespace clear
        self.client.clear_ns('bar')
        self.assertEquals(self.client.get('foo'), 1)
        self.assertEquals(self.client.get('foo', ns='bar'), None)

    def test_replace(self):
        self.client.flush_all()
        self.client.set('foo', 1, ns='bar')
        self.assertEquals(self.client.replace('foo', 2, ns='bar'), True)
        self.assertEquals(self.client.get('foo', ns='bar'), 2)

if __name__ == '__main__':
    unittest.main()
