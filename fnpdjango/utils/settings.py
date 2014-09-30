"""
Utilities for global settings.
"""
from django.utils.encoding import python_2_unicode_compatible

# Use Python3 str.
try:
    unicode
except NameError:
    pass
else:
    str = unicode


@python_2_unicode_compatible
class LazyUGettextLazy(object):
    """You can use it to internationalize strings in settings.

    Just import this class as gettext.
    """
    _ = lambda s: s
    real = False

    def __init__(self, text):
        self.text = text

    def __str__(self):
        if not self.real:
            from django.utils.translation import ugettext_lazy
            LazyUGettextLazy._ = staticmethod(ugettext_lazy)
            LazyUGettextLazy.real = True
        return str(self._(self.text))


