from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^$', apis.PostListCreateView.as_view()),
    url(r'^(?P<post_pk>\d+)/$', apis.PostDetailView.as_view()),
]