MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'fnpdjango.middleware.URLLocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

if 'django_cas' in INSTALLED_APPS:
    MIDDLEWARE_CLASSES += (
        'django_cas.middleware.CASMiddleware',
    )

MIDDLEWARE_CLASSES += (
    'django.contrib.messages.middleware.MessageMiddleware',
)

if 'piwik.django' in INSTALLED_APPS:
    MIDDLEWARE_CLASSES += (
        'piwik.django.middleware.PiwikMiddleware',
    )

MIDDLEWARE_CLASSES += (
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'pagination.middleware.PaginationMiddleware',
    # Comment out if not behind proxy setting the Real-IP header (like Nginx).
    'fnpdjango.middleware.SetRemoteAddrFromXRealIP',
)
