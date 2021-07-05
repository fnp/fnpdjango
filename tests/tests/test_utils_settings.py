# This file is part of FNPDjango, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See README.md for more information.
#
from django.conf import settings
from django.test import TestCase


class UtilsSettingsTestCase(TestCase):
    def test_lazy_ugettext_lazy(self):
        self.assertEqual(str(settings.TEST_LAZY_UGETTEXT_LAZY),
            "Lazy setting.")


