TEMPLATE_CONTEXT_PROCESSORS = tuple(x for x in (
    "django.contrib.auth.context_processors.auth"
            if "django.contrib.auth" in INSTALLED_APPS else None,
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
            if 'django.contrib.messages' in INSTALLED_APPS else None,
    "django.core.context_processors.request"
) if x is not None)
