INSTALLED_APPS = (
    '{{ project_name }}',
    'fnpdjango',
    'south',
    'pipeline',
    # Disable, if not using Piwik.
    'piwik.django',
    # Disable, if not using CAS.
    'django_cas',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)
