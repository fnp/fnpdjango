#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os
from setuptools import setup, find_packages
import sys


# Fabric needs Python 2.
if sys.version_info[0] > 2:
    from subprocess import check_call

    ve = os.environ.get('VIRTUAL_ENV')
    if not ve:
        print('Not in virtualenv!')
        sys.exit()
    subve = os.path.join(ve, 'fnpdeploy_ve')
    check_call(['virtualenv', '--python', '/usr/bin/python2.7', subve])
    check_call([os.path.join(subve, 'bin/python')] + sys.argv)

    install_requires = []
    packages = []
    package_data = {}
    scripts = ['bin/fab']
else:
    packages = ['fnpdeploy']
    package_data = {
        'fnpdeploy': ['templates/*.template'],
        }
    scripts = ['bin/git-archive-all.sh']
    install_requires = ['Fabric']


setup(
    name='fnpdeploy',
    version='0.1',
    author='Radek Czajka',
    author_email='radekczajka@nowoczesnapolska.org.pl',
    url = '',
    packages=packages,
    package_data=package_data,
    scripts=scripts,
    install_requires=install_requires,
    test_suite='nose.collector',
    tests_require=['nose'],
    license='LICENSE',
    description='.',
    long_description="",
)
