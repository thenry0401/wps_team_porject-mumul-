from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^$', apis.UserListCreateView.as_view()),
    url(r'^login/', apis.FacebookLogin.as_view(), name='fb_login')
]