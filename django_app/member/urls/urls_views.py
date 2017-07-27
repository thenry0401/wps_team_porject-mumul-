from django.conf.urls import url

from .. import views

app_name = 'member'

urlpatterns = [
    # 로그인
    url(r'^login/$', views.login, name='login'),

    # 마이 페이지, 계정 수정
    url(r'^my_page/(?P<user_pk>\d+)/$', views.my_profile, name='my_profile'),
    url(r'^my_page/edit/$', views.my_profile_edit, name='my_profile_edit')
]