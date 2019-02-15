from __future__ import unicode_literals

from django.test import TestCase
from django.template import Template, Context


class MacrosTests(TestCase):
    def test_macro(self):
        tmpl = Template("""
            {% load macros %}
            {% macro my_macro arg1 %}
            Parameter: {{ arg1 }} <br/>
            {% endmacro %}
            {% usemacro my_macro "String parameter" %}
        """)
        self.assertEqual(
            tmpl.render(Context()).strip(),
            "Parameter: String parameter <br/>"
        )
