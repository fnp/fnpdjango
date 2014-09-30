from django.db import models

from fnpdjango.storage import BofhFileSystemStorage

bofh_storage = BofhFileSystemStorage()


class SomeModel(models.Model):
    attachment = models.FileField(null=True, upload_to="test", storage=bofh_storage)
