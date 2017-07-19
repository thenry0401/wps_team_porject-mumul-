from django.conf.urls import url

from . import views

app_name = 'member'

urlpatterns = [
    url('signup/$', views.sign_up, ),
    url('login/$', name='account_login'),
    url('logout/$', name='account_logout'),
]
