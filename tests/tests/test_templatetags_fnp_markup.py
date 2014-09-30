# -*- coding: utf-8 -*-
# This file is part of FNPDjango, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See README.md for more information.
#
from __future__ import unicode_literals

import sys
from django.test import TestCase

try:
    from unittest import skipIf
except ImportError:
    # Don't need skipping for Python2.6.
    skipIf = lambda expr, comment: lambda test: test


@skipIf(sys.version_info[:2] == (3, 2),
    "No usable python-textile for Python 3.2.")
class TemplatetagsFNPMarkupTestCase(TestCase):

    def test_textile_en(self):
        from fnpdjango.templatetags import fnp_markup
        self.assertEqual(
            fnp_markup.textile_en('Test "Textile".'),
            '\t<p>Test &#8220;Textile&#8221;.</p>')
        self.assertEqual(
            fnp_markup.textile_restricted_en('Test "Textile".'),
            '\t<p>Test &#8220;Textile&#8221;.</p>')

    def test_textile_pl(self):
        from fnpdjango.templatetags import fnp_markup
        self.assertEqual(
            fnp_markup.textile_pl('Test "Textile".'),
            '\t<p>Test &#8222;Textile&#8221;.</p>')
        self.assertEqual(
            fnp_markup.textile_restricted_pl('Test "Textile".'),
            '\t<p>Test &#8222;Textile&#8221;.</p>')
