from django.conf.urls import include, url

urlpatterns = [
    url(r'^member/', include('member.urls.urls_api')),
]