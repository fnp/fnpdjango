# -*- coding: utf-8 -*-
# This file is part of FNPDjango, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See README.md for more information.
#
from __future__ import unicode_literals

from django.test import TestCase


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
