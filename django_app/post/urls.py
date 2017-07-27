from django.conf.urls import url

from post import views

app_name = 'post'
urlpatterns = [
    url(r'^list/$', views.category_post_list, name='post_list'),
    url(r'^create/$', views.post_create, name='post_create'),
]