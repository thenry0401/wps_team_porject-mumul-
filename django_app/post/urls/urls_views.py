from django.conf.urls import url

from post import views

app_name = 'post'
urlpatterns = [
    url(r'^list/$', views.post_list, name='post_list'),
    url(r'^(?P<post_pk>\d+)/detail/$', views.post_detail, name='post_detail'),
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^(?P<post_pk>\d+)/modify/$', views.post_modify, name='post_modify'),
    url(r'^(?P<post_pk>\d+)/delete/$', views.post_delete, name='post_delete'),

    url(r'^result/$', views.post_search_result, name='post_search_result'),

    url(r'^(?P<post_pk>\d+)/comment/create/$', views.comment_create, name='comment_create'),
    url(r'^comment/(?P<comment_pk>\d+)/modify/$', views.comment_modify, name='comment_modify'),
    url(r'^comment/(?P<comment_pk>\d+)/delete/$', views.comment_delete, name='comment_delete'),
]