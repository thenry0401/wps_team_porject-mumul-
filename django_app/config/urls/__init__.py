from django.conf.urls import url, include
from . import url_apis, url_views

urlpatterns = [
    # /....은 url_views.py의 url_patterns를 사용
    # /apis/...은 urls_apis.py의 url_patterns를 사용

    # url(r'', include(url_views)),
    url(r'', include(url_apis)),
]