"""
Utilities for global settings.
"""
from django.utils.functional import Promise


class LazyUGettextLazy(Promise):
    """You can use it to internationalize strings in settings.

    Just import this class as gettext.
    """
    _ = lambda s: s
    real = False

    def __init__(self, text):
        self.text = text

    def __str__(self):
        if not self.real:
            from django.utils.translation import gettext_lazy
            LazyUGettextLazy._ = staticmethod(gettext_lazy)
            LazyUGettextLazy.real = True
        return str(self._(self.text))


