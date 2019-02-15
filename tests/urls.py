from django.conf.urls import url
from fnpdjango.utils.urls import i18n_patterns
from . import views


urlpatterns = [
    url(r'^ip/$', views.ip),
] + i18n_patterns(
    url(r'^$', views.get_lang),
)
