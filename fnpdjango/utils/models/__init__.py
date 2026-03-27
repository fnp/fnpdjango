"""
Utilities for Django models.
"""

from django.utils.functional import lazy


concat_lazy = lazy(lambda *args: ''.join(str(arg) for arg in args), str)


def filtered_model(name, model, field, value, verbose_extra=None):
    """Creates a proxy model filtering objects by a field."""
    verbose_extra = verbose_extra or value
    class  Meta:
        proxy = True
        app_label = model._meta.app_label
        verbose_name = concat_lazy(model._meta.verbose_name, ': ', verbose_extra)
        verbose_name_plural = concat_lazy(model._meta.verbose_name_plural, ': ', verbose_extra)

    def save(self, *args, **kwargs):
        if not getattr(self, field):
            setattr(self, field, value)
        return model.save(self, *args, **kwargs)

    attrs = {'__module__': '', 'Meta': Meta, 'save': save}
    return type(name, (model,), attrs)
