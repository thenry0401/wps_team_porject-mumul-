from django.conf.urls import include, url

urlpatterns = [
    url(r'^member/', include('member.urls.urls_api')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^post/', include('post.urls.urls_apis')),
]