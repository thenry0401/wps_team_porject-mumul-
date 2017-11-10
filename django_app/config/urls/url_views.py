"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from .. import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts/', include('allauth.urls'), name='account'),
    url(r'^member/', include('member.urls.urls_views')),
    url(r'^admin/', admin.site.urls),

    url(r'^post/', include('post.urls.urls_views')),

    # url(r'^api-token-auth/', obtain_auth_token),
]

# /static/에 대한 요청을 STATIC_ROOT 경로의 파일에서 찾는다
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# /media/에 대한 요청을 MEDIA_ROOT 경로의 파일에서 찾는다
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
