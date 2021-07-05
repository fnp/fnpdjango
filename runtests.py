#!/usr/bin/env python
# This file is part of FNPDjango, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See README.md for more information.
#
"""
Creates a simple Django configuration and runs tests for fnpdjango.
"""
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

                'NAME': 'test.db',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.messages',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.staticfiles',

            'fnpdjango',
            'tests',
        ],
        LANGUAGE_CODE='pl',
        MEDIA_ROOT=media_root,
        STATIC_URL='/static/',
        STATIC_ROOT='./static/',
        STATICFILES_STORAGE = 'fnpdjango.pipeline_storage.GzipPipelineManifestStorage',
        MIDDLEWARE=[
            'django.middleware.common.CommonMiddleware',
            'fnpdjango.middleware.SetRemoteAddrFromXRealIP',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ],
        FNPDJANGO_REALIP = True,
        ROOT_URLCONF='tests.urls',
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ]
                }
            },
        ],
        TEST_LAZY_UGETTEXT_LAZY=_("Lazy setting."),
        USE_I18N=True,

        SECRET_KEY='x',
        DEBUG=True,
        SITE_ID=1,

        PIPELINE={}
    )
else:
    media_root = None

from django.test.runner import DiscoverRunner


def runtests(*test_args, **kwargs):
    """Actual test suite entry point."""
    if not test_args:
        test_args = ['tests']
    parent = dirname(abspath(__file__))
    sys.path.insert(0, parent)

    from django import setup
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
