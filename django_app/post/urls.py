from django.conf.urls import url

from post import views

app_name = 'post'

urlpatterns = [
    url(r'^create/$', views.post_create, name='post_create'),
    url(r'^result/$', views.post_search_result, name='post_search_result'),
]