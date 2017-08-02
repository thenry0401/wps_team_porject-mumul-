from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from .. import views

app_name = 'member'

urlpatterns = [
    # 로그인, 로그아웃, 회원가입
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^naver-login-test/$', views.naver_login_test, name='naver_login_test'),

    # 마이 페이지, 계정 수정
    url(r'^my_page/(?P<user_pk>\d+)/$', views.my_profile, name='my_profile'),
    url(r'^my_page/edit/$', views.my_profile_edit, name='my_profile_edit')
]