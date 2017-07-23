from django.conf.urls import include, url

urlpatterns = [
    url(r'^member/', include('member.urls.urls_api')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/facebook/', include('member.urls.urls_api'))
]