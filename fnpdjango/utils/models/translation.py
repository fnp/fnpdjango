"""
Utilities for creating multilingual fields in your apps.
"""

from copy import copy
from django.conf import settings
from django.db import models
from django.utils.translation import get_language, string_concat


def localize_field(name, lang=None):
    if lang is None:
        lang = get_language()
    if lang not in (x[0] for x in settings.LANGUAGES):
        lang = settings.LANGUAGE_CODE
    return "%s_%s" % (name, lang)

def field_getter(name):
    @property
    def getter(self):
        val = getattr(self, localize_field(name), None)
        if not val:
            val = getattr(self, localize_field(name, settings.LANGUAGE_CODE))
        return val
    return getter


def add_translatable(model, fields, languages=None):
    """Adds some translatable fields to a model, and a getter."""
    if languages is None:
        languages = settings.LANGUAGES
    for name, field in fields.items():
        for lang_code, lang_name in languages:
            new_field = copy(field)
            if field.verbose_name:
                new_field.verbose_name = string_concat(field.verbose_name, ' [%s]' % lang_code)
            new_field.contribute_to_class(model, localize_field(name, lang_code))
        setattr(model, name, field_getter(name))
        # add setter?


def add_translatable_index(index_class, fields, languages=None):
    """Adds some translatable fields to a search index."""
    if languages is None:
        languages = settings.LANGUAGES
    for name, field in fields.items():
        for lang_code, lang_name in languages:
            new_field = copy(field)
            fname = localize_field(name, lang_code)
            new_field.index_fieldname = new_field.index_fieldname \
                and localize_field(new_field.index_fieldname, lang_code) \
                or fname
            new_field.model_attr = new_field.model_attr \
                and localize_field(new_field.model_attr, lang_code) \
                or fname
            setattr(index_class, fname, new_field)
            index_class.fields[fname] = new_field


def translated_fields(field_names, languages=settings.LANGUAGES):
    """Generate a tuple of field names in translated versions."""
    return tuple(localize_field(field_name, lang_code)
                for field_name in field_names
                for lang_code, lang_name in languages
                )

def tQ(**kwargs):
    """ Creates a query (Q) with lookups on translated fields. """
    trans_kwargs = {}
    for k, v in kwargs.items():
        trans_kwargs[localize_field(k)] = v
    return models.Q(**trans_kwargs)
