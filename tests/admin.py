from django.contrib import admin
from . import models
from fnpdjango import actions


class SomeModelAdmin(admin.ModelAdmin):
    actions = [
        actions.export_as_csv_action("CSV")
    ]


admin.site.register(models.SomeModel, SomeModelAdmin)

