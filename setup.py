#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

long_description = """Python module helps to perform a lot of HTTP queries using the onion router."""

setup(name='torquery',
      version='0.3.1',
      description='TOR HTTP queries handler',
      author='Lorenzo Setale ( http://who.is.lorenzo.setale.me/? )',
      author_email='koalalorenzo@gmail.com',
      url='https://github.com/koalalorenzo/torquery',
      packages=['torquery'],
      install_requires=['stem'],
      long_description=long_description
     )
