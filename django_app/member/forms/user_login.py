from allauth.account.auth_backends import AuthenticationBackend
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': '이메일 입력하세요',
                'required': 'True',
            }
        ), label="이메일"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력하세요',
                'required': 'True',
            }
        ), label="비밀번호"
    )

    class Meta:
        model = User
        fields = ["email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # authenticate() 함수는 settings의 AUTHENTICATION_BACKENDS 항목에 등록된 인증 체계 기반 클래스를 하나씩 가져와서 인증을 시도합니다.
        user = AuthenticationBackend._authenticate_by_email(
            self=self,
            email=email,
            password=password,
        )
        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError(
                '로그인 정보가 일치하지 않습니다.',
            )
        return self.cleaned_data
