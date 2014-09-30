#!/usr/bin/env python
# -*- coding: utf-8
# This file is part of FNPDjango, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See README.md for more information.
#
"""
Creates a simple Django configuration and runs tests for fnpdjango.
"""
from __future__ import unicode_literals

import sys
import os
from os.path import dirname, abspath
from optparse import OptionParser
from shutil import rmtree

from django.conf import settings
from fnpdjango.utils.settings import LazyUGettextLazy as _


# For convenience configure settings if they are not pre-configured or if we
# haven't been provided settings to use by environment variable.
if not settings.configured and not os.environ.get('DJANGO_SETTINGS_MODULE'):
    import tempfile
    media_root = tempfile.mkdtemp(prefix='djangotest_')

    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',

            'fnpdjango',
            'tests',
        ],
        LANGUAGE_CODE='pl',
        MEDIA_ROOT=media_root,
        TEST_LAZY_UGETTEXT_LAZY=_("Lazy setting."),
    )
else:
    media_root = None

try:
    from django.test.runner import DiscoverRunner
except ImportError:
    # Django < 1.6
    from django.test.simple import DjangoTestSuiteRunner as DiscoverRunner


def runtests(*test_args, **kwargs):
    """Actual test suite entry point."""
    if not test_args:
        test_args = ['tests']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)

    # For Django 1.7+
    try:
        from django import setup
    except ImportError:
        pass
    else:
        setup()

    test_runner = DiscoverRunner(
        verbosity=kwargs.get('verbosity', 1),
        interactive=kwargs.get('interactive', False),
        failfast=kwargs.get('failfast'))
    failures = test_runner.run_tests(test_args)
    if media_root:
        rmtree(media_root)
    sys.exit(failures)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--failfast', action='store_true',
                      default=False, dest='failfast')

    (options, args) = parser.parse_args()

    runtests(failfast=options.failfast, *args)
