from django.http import HttpResponse


def ip(request):
    return HttpResponse(request.META['REMOTE_ADDR'])
