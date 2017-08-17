from django.conf.urls import url
from member import apis as member_apis
from .. import apis

urlpatterns = [
    url(r'^list/$', apis.PostListCreateView.as_view(), name='post_list'),
    url(r'^tag/(?P<tag_name>\w+)/$', apis.HashtagPostListView.as_view(), name='hashtag_post_list'),
    url(r'^create/$', apis.PostListCreateView.as_view(), name='post_create'),

    url(r'^(?P<post_pk>\d+)/$', apis.PostDetailView.as_view()),

    url(r'^(?P<post_pk>\d+)/comment/create/$', apis.CommentListCreateView.as_view(), name='comment_create'),
    url(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/$', apis.CommentDetailView.as_view(), name='comment_detail'),
    url(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/modify/$', apis.CommentDetailView.as_view(), name='comment_modify'),
    url(r'^(?P<post_pk>\d+)/comment/(?P<comment_pk>\d+)/delete/$', apis.CommentDetailView.as_view(), name='comment_delete'),

    # ##### 위시리스트 추가/삭제 #####
    url(r'^(?P<post_pk>[0-9]+)/wish-list/toggle/$', apis.PostLikeToggleView.as_view(), name='wishlist-toggle'),

    #### 매물 등록/삭제
    url(r'^(?P<post_pk>[0-9]+)/for-sale/toggle/$', apis.ForSaleToggleView.as_view(), name='for_sale_toggle'),
]