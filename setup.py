# -*- coding: utf-8 -*-

import nsmemcached

from distutils.core import setup


setup(
    name='NSMemcached',
    version=nsmemcached.__version__,
    description='A simple implementation of a namespaced memcached client',
    author='Nicolas Perriault',
    author_email='np@akei.com',
    packages=['nsmemcached', ],
    requires=['python_memcached (>=1.47, <2.0)', ],
    license='MIT',
    long_description=open('README.rst').read(),
)
