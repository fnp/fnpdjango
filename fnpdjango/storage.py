# -*- coding: utf-8 -*-
# This file is part of FNPDjango, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
from django.core.files.storage import FileSystemStorage

class BofhStorageMixin(FileSystemStorage):
    """Bastard Operator From Hell file storage for Django.

    When a user asks for a place available for saving a file and
    the proposed filename is occupied, default Django file storage
    looks for a free spot by appending a suffix.

    This storage just deletes the previous content and replies:
    sure, just save it right where you want it.

    The user is now responsible for making sure they don't
    accidentally overwrite anything they weren't supposed to,
    and for sane caching settings.

    """
    def get_available_name(self, name):
        if self.exists(name):
            self.delete(name)
        return name

class BofhFileSystemStorage(BofhStorageMixin, FileSystemStorage):
    """Bastard Operator From Hell storage for standard filesystem."""
    pass
