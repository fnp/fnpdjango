# This file is part of FNPDjango, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See README.md for more information.
#
from django.test import TestCase
from django.test.utils import override_settings


class TemplatetagsFNPAnnoyTestCase(TestCase):

    def test_annoy(self):
        from fnpdjango.templatetags import fnp_annoy
        self.assertEqual(
            fnp_annoy.annoy(),
            '')
        with override_settings(FNP_ANNOY=True):
            self.assertTrue(
                'https://nowoczesnapolska.org.pl/pomoz-nam/1-procent/'
                in fnp_annoy.annoy()
            )
