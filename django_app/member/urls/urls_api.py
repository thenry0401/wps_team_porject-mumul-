from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt

from .. import apis

urlpatterns = [
    url(r'^$', apis.UserListView.as_view(), name='user_list'),
    url(r'^login/', apis.UserLoginView.as_view(), name='login'),
    url(r'^facebook/login/', csrf_exempt(apis.FacebookLoginView.as_view()), name='fb_login'),
]