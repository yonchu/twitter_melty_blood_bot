#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

AUTHOR = 'Yonchu'
AUTHOR_EMAIL = 'yuyuchu3333@gmail.com'
VERSION = '0.0.1'
LICENSE = 'MIT'

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
#CHANGES = open(os.path.join(here, 'CHANGES')).read()

requires = ['tweepy',
            'SQLAlchemy',
            'google-api-python-client']

classifiers = ['Development Status :: 3 - Alpha',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: MIT License',
               'Operating System :: POSIX',
               'Programming Language :: Python',
               'Topic :: Internet']

if __name__ == '__main__':
    setup(name='twitter_bot',
          packages=find_packages(exclude=['samples', '*.tests', '*.tests.*',
                                          'tests.*', 'tests']),
          include_package_data=True,
          version=VERSION,
          description='Twitter bot',
          long_description=README,
          test_suite='tests',
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          url='http://github.com/yonchu/twitter_melty_blood_bot',
          keywords='twitter bot melty blood',
          license=LICENSE,
          install_requires=requires,
          classifiers=classifiers,
          zip_safe=False)
