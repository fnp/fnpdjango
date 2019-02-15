from django.http import HttpResponse
from django.utils.translation import get_language


def get_lang(request):
    return HttpResponse(get_language())


def ip(request):
    return HttpResponse(request.META['REMOTE_ADDR'])
