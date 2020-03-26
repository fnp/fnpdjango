from django.conf.urls import url
from django.contrib import admin
from fnpdjango.utils.urls import i18n_patterns
from . import views


# For Django < 1.7.
admin.autodiscover()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ip/$', views.ip),
] + i18n_patterns(
    url(r'^$', views.get_lang),
)
