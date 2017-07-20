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
        User.objects.get_or_create_facebook_user(user_pk=user.pk)
        # url = sociallogin.account.get_avatar_url() # 페이스북 프로필 이미지 획득 URL

        return user
