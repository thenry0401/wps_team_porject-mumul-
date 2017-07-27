from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

# Create your views here.
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from rest_auth.registration.views import SocialLoginView

from member.forms.user_edit import UserEditForm

User = get_user_model()


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        allauth를 통해서 유저를 저장할 때 호출됩니다. 유저 객체에 추가적인 정보를 담기 위해서 오버라이드를 실시했습니다.
        """

        user = super(SocialAccountAdapter, self).save_user(request, sociallogin, form)

        # (하드코딩) social_app_name = str(request.path).split("/")[2].upper()
        social_app_name = sociallogin.account.provider.upper()
        extra_data = sociallogin.account.extra_data
        if social_app_name == "FACEBOOK":
            profile_url = "https://graph.facebook.com/v2.4/{user_id}/picture?type=square&height={height}&width={width}&return_ssl_rources=1".format(
                user_id=extra_data['id'],
                height=150,
                width=150,
            )
            User.objects.get_or_create_facebook_user(user_pk=user.pk, extra_data=extra_data, profile_url=profile_url)

        elif social_app_name == "NAVER":
            User.objects.get_or_create_naver_user(user_pk=user.pk, extra_data=extra_data)

        return user


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


def my_profile(request, user_pk=None):

    if not request.user.is_authenticated and not user_pk:
        login_url = reverse('accounts:login')
        redirect_url = login_url + '?next=' + request.get_full_path()
        return redirect(redirect_url)

    if user_pk:
        user = get_object_or_404(User, pk=user_pk)
    else:
        user = request.user
    context = {
        'cur_user': user
    }

    return render(request, 'member/my_profile.html', context)

@login_required
def my_profile_edit(request):
    if request.method == "POST":
        form = UserEditForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user
        )
        if form.is_valid():
            form.save()
            return redirect('member:my_profile_edit')

    else:
        form = UserEditForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'member/my_profile_edit.html', context)

