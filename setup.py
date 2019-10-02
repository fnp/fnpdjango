#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os.path
from setuptools import setup, find_packages


def whole_trees(package_dir, paths):
    def whole_tree(prefix, path):
        files = []
        for f in (f for f in os.listdir(os.path.join(prefix, path)) if f[0] != '.'):
            new_path = os.path.join(path, f)
            if os.path.isdir(os.path.join(prefix, new_path)):
                files.extend(whole_tree(prefix, new_path))
            else:
                files.append(new_path)
        return files
    prefix = os.path.join(os.path.dirname(__file__), package_dir)
    files = []
    for path in paths:
        files.extend(whole_tree(prefix, path))
    return files

setup(
    name='fnpdjango',
    version='0.4.3',
    author='Radek Czajka',
    author_email='radekczajka@nowoczesnapolska.org.pl',
    url='',
    packages=find_packages(exclude=['tests*']),
    package_data={
        'fnpdjango': whole_trees('fnpdjango', ['templates', 'locale', 'static']),
        'fnpdjango.management.commands': ['babel.cfg'],
    },
    install_requires=[
        'Django>=1.4,<2.3',
    ],
    extras_require={
        'textile': [
            'textile==2.3.16',
        ],
        'pipeline': [
            'pipeline',
        ],
    },
    license='LICENSE',
    description='.',
    long_description="",
    test_suite="runtests.runtests",
)
