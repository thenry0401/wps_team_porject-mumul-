import requests
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

# Create your views here.
from django.contrib.auth import get_user_model

User = get_user_model()

class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        This is called when saving user via allauth registration.
        We override this to set additional data on user object.
        """

        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)

        # 유저가 저장되기 전, request.path를 통해 app_name을 검출한다.
        # app_name을 통해서 user_type을 결정해줘야 하므로 이러한 방법을 사용했다.
        social_app_name = str(request.path).split("/")[2].upper()
        # print(social_app_name)
        # print(sociallogin.account.extra_data)
        if social_app_name == "FACEBOOK":
            # url = sociallogin.account.get_avatar_url() # 페이스북 프로필 이미지 획득 URL
            User.objects.get_or_create_facebook_user(user_pk=user.pk)

        elif social_app_name == "NAVER":
            extra_data = sociallogin.account.extra_data
            User.objects.get_or_create_naver_user(user_pk=user.pk, extra_data=extra_data)


        # print("dir(sociallogin : ", dir(sociallogin))
        # print("dir(sociallogin.account) : ", dir(sociallogin.account))
        # print("sociallogin.account.extra_data : ", sociallogin.account.extra_data)

        return user
