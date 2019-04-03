# -*- coding: utf-8 -*-
# This file is part of FNPDjango, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See README.md for more information.
#
"""
This file works only for django.test.simple.DjangoTestSuiteRunner
in Django<1.6.  The newer django.test.runner.DiscoverRunner finds
test_* modules by itself.

"""
from .test_middleware import *
from .test_storage import *
from .test_templatetags_fnp_annoy import *
from .test_templatetags_fnp_markup import *
from .test_templatetags_macros import *
from .test_utils_settings import *
from .test_utils_urls import *
