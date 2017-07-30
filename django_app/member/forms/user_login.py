from django import forms
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '아이디를 입력하세요',
            }
        ), label="아이디"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력하세요',
            }
        ), label="비밀번호"
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        # authenticate() 함수는 settings의 AUTHENTICATION_BACKENDS 항목에 등록된 인증 체계 기반 클래스를 하나씩 가져와서
        # authenticate() 메서드를 호출하여 인증을 시도합니다.
        user = authenticate(
            username=username,
            password=password,
        )
        if user is not None:
            self.cleaned_data['user'] = user
        else:
            raise forms.ValidationError(
                'Login credential not valid'
            )
        return self.cleaned_data
