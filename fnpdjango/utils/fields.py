from django.forms import CharField, ValidationError
from .text.textilepl import textile_pl

try:
    from markupfield.fields import MarkupField
except ImportError:
    MarkupField = None
else:
    def validate_textile(value):
        try:
            textile_pl(value)
        except Exception:
            raise ValidationError('Syntax error in markup.')


    class TextileFormField(CharField):
        default_validators = [validate_textile]


    class TextileField(MarkupField):
        def formfield(self, **kwargs):
            defaults = {'form_class': TextileFormField}
            defaults.update(kwargs)
            return super(MarkupField, self).formfield(**defaults)
