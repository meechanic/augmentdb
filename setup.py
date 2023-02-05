#!/usr/bin/env python

from distutils.core import setup

setup(name='augmentdb',
  version='0.0.1',
  description='AugmentDB',
  author='Mikhail Efremov',
  author_email='meechanic.design@gmail.com',
  url='https://github.com/meechanic',
  license="MIT",
  scripts=['bin/augdb-enrich', 'bin/augdb-enrich-by-ids', 'bin/augdb-get', 'bin/augdb-ls', 'bin/augdb-objmerge', 'bin/augdb-objmerge-with-db', 'bin/augdb-stat'],
  packages=['augmentdb']
)
