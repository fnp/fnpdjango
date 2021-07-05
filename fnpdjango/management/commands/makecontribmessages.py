# This file is part of FNPDjango, licensed under GNU Affero GPLv3 or later.
# Copyright © Fundacja Nowoczesna Polska. See NOTICE for more information.
#
import os
from optparse import make_option
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Builds .po files for contrib apps.'

    def handle(self, **options):
        from django.conf import settings

        if not hasattr(settings, 'CONTRIB_LOCALE_APPS') or not settings.CONTRIB_LOCALE_APPS:
            print("CONTRIB_LOCALE_APPS not set, no contrib locale needed.")
            return

        from subprocess import call
        import babel

        app_names = settings.CONTRIB_LOCALE_APPS
        print('L10n for:', ", ".join(app_names))
        app_dirs = [os.path.dirname(__import__(app).__file__)
                        for app in app_names]
        assert settings.LOCALE_PATHS
        locale_path = settings.LOCALE_PATHS[0]
        print('Using:', locale_path)

        # Create the POT file.
        babel_cfg = os.path.join(locale_path,  "babel.cfg")
        if not os.path.exists(babel_cfg):
            babel_cfg = os.path.join(os.path.dirname(__file__), 'babel.cfg')
        pot_path = os.path.join(locale_path,  "django.pot")
        call(["pybabel", "extract",
                "-F", babel_cfg,
                "-o", pot_path] + app_dirs)

        # Lose the unneeded absolute file paths in the POT.
        with open(pot_path) as f:
            pot = f.read()
        for i, app_dir in enumerate(app_dirs):
            pot = pot.replace("\n#: " + app_dir, "\n#: " + app_names[i])
        with open(pot_path, 'w') as f:
            f.write(pot)

        # Create/update the PO files.
        call(["pybabel", "update", "-D", "django",
                "-i", pot_path,
                "-d", locale_path])
