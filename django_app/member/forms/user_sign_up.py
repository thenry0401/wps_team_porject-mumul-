from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserSignUpForm(UserCreationForm):

    name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': '실명을 입력하세요',
            }
        ), label="성함"
    )

    class Meta:
        model = User
        fields = ('email', 'name', 'nickname')


    def signup(self, request, user):
        user.email = self.cleaned_data["email"]
        user.nickname = self.cleaned_data['nickname']
        user.name = self.cleaned_data['name']
        user.save()

        return user
