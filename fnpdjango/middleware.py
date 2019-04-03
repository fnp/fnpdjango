from . import app_settings

try:
    # Django >= 1.10
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    # Django <= 1.9
    MiddlewareMixin = object

    from django.conf import settings
    from django.http import Http404
    from django.utils import translation

    class URLLocaleMiddleware(MiddlewareMixin):
        """Decides which translation to use, based on path only."""
        def process_request(self, request):
            language = translation.get_language_from_path(request.path_info)
            if language:
                translation.activate(language)
            request.LANGUAGE_CODE = translation.get_language()
            if language == settings.LANGUAGE_CODE:
                raise Http404

        def process_response(self, request, response):
            language = translation.get_language()
            translation.deactivate()
            if 'Content-Language' not in response:
                response['Content-Language'] = language
            return response
else:
    # Django >= 1.10
    import warnings
    from django.middleware.locale import LocaleMiddleware

    class URLLocaleMiddleware(LocaleMiddleware):
        def __init__(self, *args, **kwargs):
            warnings.warn(
                "As of Django 1.10, fnpdjango.middleware.URLLocaleMiddleware "
                "is deprecated in favor of "
                "django.middleware.locale.LocaleMiddleware.",
                DeprecationWarning)
            super(URLLocaleMiddleware, self).__init__(*args, **kwargs)


class SetRemoteAddrFromXRealIP(MiddlewareMixin):
    """Sets REMOTE_ADDR from the X-Real-IP header, as set by Nginx."""
    def process_request(self, request):
        if app_settings.REALIP:
            try:
                request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
            except KeyError:
                pass
        return None
