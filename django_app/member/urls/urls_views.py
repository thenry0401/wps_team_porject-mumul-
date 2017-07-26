from django.conf.urls import url

from .. import views

app_name = 'member'

urlpatterns = [
    url(r'^my_page/$', views.my_profile, name='my_profile'),
    url(r'^my_page/edit/(?P<user_pk>\d+)/$', views.my_profile_edit, name='my_profile_edit')
]