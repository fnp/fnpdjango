# This file is part of FNPDjango, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See README.md for more information.
#
from tempfile import NamedTemporaryFile
from django.core.files.base import ContentFile
from django.test import TestCase
from tests.models import SomeModel


class StorageTestCase(TestCase):
    def test_save(self):
        obj = SomeModel.objects.create()
        obj.attachment.save("text.txt", ContentFile(b"A"))
        path = obj.attachment.path
        self.assertEqual(open(path, 'rb').read(), b"A")
        # Now save again under the same filename.
        obj.attachment.save("text.txt", ContentFile(b"B"))
        self.assertEqual(open(path, 'rb').read(), b"B")
