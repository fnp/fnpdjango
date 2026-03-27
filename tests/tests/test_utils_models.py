from django.db import models
from django.test import SimpleTestCase
from django.utils.translation import gettext_lazy as _

from fnpdjango.utils.models import filtered_model
from fnpdjango.utils.models.translation import add_translatable


class UtilsModelsTestCase(SimpleTestCase):
    def test_filtered_model_uses_lazy_verbose_names(self):
        class BaseModel(models.Model):
            status = models.CharField(max_length=32, blank=True)

            class Meta:
                app_label = 'tests'
                verbose_name = _('base item')
                verbose_name_plural = _('base items')

        ProxyModel = filtered_model('ProxyModel', BaseModel, 'status', 'published', _('published'))

        self.assertEqual(str(ProxyModel._meta.verbose_name), 'base item: published')
        self.assertEqual(str(ProxyModel._meta.verbose_name_plural), 'base items: published')

    def test_add_translatable_preserves_lazy_verbose_name(self):
        class Article(models.Model):
            class Meta:
                app_label = 'tests'

        add_translatable(
            Article,
            {
                'title': models.CharField(_('Title'), max_length=255),
            },
            languages=[('pl', 'Polish'), ('en', 'English')],
        )

        self.assertEqual(str(Article._meta.get_field('title_pl').verbose_name), 'Title [pl]')
        self.assertEqual(str(Article._meta.get_field('title_en').verbose_name), 'Title [en]')
