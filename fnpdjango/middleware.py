from django.utils.deprecation import MiddlewareMixin
from . import app_settings


class SetRemoteAddrFromXRealIP(MiddlewareMixin):
    """Sets REMOTE_ADDR from the X-Real-IP header, as set by Nginx."""
    def process_request(self, request):
        if app_settings.REALIP:
            try:
                request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
            except KeyError:
                pass
        return None
