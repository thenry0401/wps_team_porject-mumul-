from django.conf.urls import url, include
from . import url_apis, url_views

urlpatterns = [
    url(r'', include(url_apis)),
]