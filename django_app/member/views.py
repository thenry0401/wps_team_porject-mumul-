from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import render, redirect


# Create your views here.
class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        return redirect("base:index")

    def get_logout_redirect_url(self, request):
        return redirect("base:index")

def sign_up(request):
    return render(request, 'account:account_signup')