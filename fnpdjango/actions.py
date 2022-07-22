# Source: https://gist.github.com/jeremyjbowers/e8d007446155c12033e6
import csv
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


def export_as_csv_action(description=_("Export selected objects as CSV file"), fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = fields or [field.name for field in opts.fields]

        if exclude:
            field_names = [f for f in field_names if f not in exclude]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % str(opts).replace('.', '_')

        writer = csv.writer(response)

        if header:
            writer.writerow(field_names)
        for obj in queryset:
            row = []
            for field in field_names:
                value = getattr(obj, field)
                if callable(value):
                    value = value()
                row.append(str(value))
            writer.writerow(row)

        return response

    export_as_csv.short_description = description
    return export_as_csv

