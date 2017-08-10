from django.conf.urls import url
from member import apis as member_apis
from .. import apis

urlpatterns = [
    url(r'^list/$', apis.PostListCreateView.as_view(), name='post_list'),
    url(r'^create/$', apis.PostListCreateView.as_view(), name='post_create'),

    url(r'^(?P<post_pk>\d+)/$', apis.PostDetailView.as_view()),


    # ##### 위시리스트 추가/삭제 #####
    url(r'^(?P<pk>[0-9]+)/wish-list/toggle/$', member_apis.PostLikeToggle.as_view(), name='wishlist-toggle'),
]