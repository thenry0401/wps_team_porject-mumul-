from django.conf.urls import url
from member import apis as member_apis
from .. import apis

urlpatterns = [
    url(r'^list/$', apis.PostListCreateView.as_view(), name='post_list'),
    url(r'^create/$', apis.PostListCreateView.as_view(), name='post_create'),


    url(r'^(?P<post_pk>\d+)/$', apis.PostDetailView.as_view()),

    url(r'^(?P<post_pk>\d+)/comment-create/$', apis.CommentListCreateView.as_view(), name='comment_create'),


    # ##### 위시리스트 추가/삭제 #####
    url(r'^(?P<post_pk>\d+)/like-toggle/$', apis.PostLikeToggleView.as_view(), name='wishlist_toggle'),

]