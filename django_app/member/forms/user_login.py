from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
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

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # authenticate() 함수는 settings의 AUTHENTICATION_BACKENDS 항목에 등록된 인증 체계 기반 클래스를 하나씩 가져와서
        # authenticate() 메서드를 호출하여 인증을 시도합니다.
        user = authenticate(
            email=email,
            password=password,
        )
        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError(
                'Login credential not valid'
            )
        return self.cleaned_data
