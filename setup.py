#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import os.path
from setuptools import setup, find_packages

def whole_trees(package_dir, paths):
    def whole_tree(prefix, path):
        files = []
        for f in (f for f in os.listdir(os.path.join(prefix, path)) if not f[0]=='.'):
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
    version='0.1.14',
    author='Radek Czajka',
    author_email='radekczajka@nowoczesnapolska.org.pl',
    url = '',
    packages=find_packages(),
    package_data={
        'fnpdjango': whole_trees('fnpdjango', ['templates', 'locale']),
        'fnpdjango.deploy': ['templates/*.template'],
        'fnpdjango.management.commands': ['babel.cfg'],
    },
    scripts=[
        'bin/git-archive-all.sh',
        'bin/fnpdjango_bootstrap.sh',
    ],
    install_requires=[
        'django>=1.4,<1.7',
        'textile',
    ],
    license='LICENSE',
    description='.',
    long_description="",
)
