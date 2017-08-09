from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^$', apis.UserListView.as_view(), name='user_list'),

    # 유저 회원가입
    url(r'^register/', apis.UserListView.as_view(), name='user_create'),

    # 유저 Retrieve, Update, Destroy
    url(r'^(?P<pk>\d+)/$', apis.UserRetrieveUpdateDestroyView.as_view()),

    # 로그인 관련 처리 뷰
    url(r'^login/', apis.UserLoginView.as_view(), name='login'),
    url(r'^fb-login/$', apis.FacebookLogin.as_view(), name='fb_login'),
    url(r'^naver-login/$', apis.NaverLogin.as_view(), name='nv_login'),

]