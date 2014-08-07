#!/usr/bin/env python
# -*- coding: utf8 -*-
"""
Easily spoof your MAC address in OS X, Windows & Linux.
"""
from setuptools import setup, find_packages


def get_version():
    """
    Load and return the current package version.
    """
    local_results = {}
    execfile('spoofmac/version.py', {}, local_results)
    return local_results['__version__']


if __name__ == '__main__':
    setup(
        name='SpoofMAC',
        version=get_version(),
        description=__doc__,
        long_description=__doc__,
        author='Feross Aboukhadijeh',
        author_email='feross@feross.org',
        url='http://feross.org/spoofmac/',
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            'docopt'
        ],
        scripts=[
            'scripts/spoof-mac'
        ],
        license='MIT'
    )
