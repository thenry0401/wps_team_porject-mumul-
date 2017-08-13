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

    #################
    ## 마이 페이지
    #################

    # 유저가 좋아요 한 목록
    url(r'wish-list/', apis.MyWishList.as_view(), name='user_wishlist'),

    #################
    ## 팔로잉 토글
    #################

    # 팔로잉 / 언팔로잉
    url(r'^follow-toggle/(?P<user_pk>\d+)/$', apis.FollowingToggle.as_view(), name='following_toggle'),

]