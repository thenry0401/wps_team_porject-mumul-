from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^$', apis.UserListView.as_view(), name='user_list'),
    url(r'^login/', apis.UserLoginView.as_view(), name='login'),
    url(r'^fb-login/$', apis.FacebookLoginView.as_view(), name='fb_login'),
    url(r'^naver-login/$', apis.NaverLoginView.as_view(), name='nv_login'),

    url(r'^register/', apis.UserCreateView.as_view(), name='user_create'),
    # url(r'^user-edit/$', )
]