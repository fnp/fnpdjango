from . import INSTALLED_APPS


MIDDLEWARE_CLASSES = tuple(x for x in (
    'django.contrib.sessions.middleware.SessionMiddleware'
            if "django.contrib.sessions" in INSTALLED_APPS else None,
    #'django.middleware.locale.LocaleMiddleware',
    'fnpdjango.middleware.URLLocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware'
            if "django.contrib.auth" in INSTALLED_APPS else None,
    'django_cas.middleware.CASMiddleware'
            if "django_cas" in INSTALLED_APPS else None,
    'django.contrib.messages.middleware.MessageMiddleware'
            if "django.contrib.messages" in INSTALLED_APPS else None,
    'piwik.django.middleware.PiwikMiddleware'
            if "piwik.django" in INSTALLED_APPS else None,
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware'
            if "pagination" in INSTALLED_APPS else None,
    'fnpdjango.middleware.SetRemoteAddrFromXRealIP'
) if x is not None)
