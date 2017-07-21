import requests
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

# Create your views here.
from django.contrib.auth import get_user_model

User = get_user_model()

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        allauth를 통해서 유저를 저장할 때 호출됩니다.
        유저 객체에 추가적인 정보를 담기 위해서 오버라이드를 실시했습니다.
        """

        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)

        # (하드코딩) social_app_name = str(request.path).split("/")[2].upper()
        social_app_name = sociallogin.account.provider.upper()

        if social_app_name == "FACEBOOK":
            profile_url = sociallogin.account.get_avatar_url() # 페이스북 프로필 이미지 획득 URL
            User.objects.get_or_create_facebook_user(user_pk=user.pk, profile_url=profile_url)

        elif social_app_name == "NAVER":
            extra_data = sociallogin.account.extra_data
            User.objects.get_or_create_naver_user(user_pk=user.pk, extra_data=extra_data)

        return user
