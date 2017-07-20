from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from django.conf.urls import url

from member import views

app_name = 'member'

urlpatterns = [
    url(r'^naver/$', views.complete_login, name="naver_login_by_token"),
]
