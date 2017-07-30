from django import forms


class UserSignUpForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': '이메일을 입력하세요'
            }
        ), label="이메일"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 입력하세요',
            }
        ), label="비밀번호"
    )

    password_confirm = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '비밀번호를 확인합니다.',
            }
        ), label="비밀번호 검증"
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '실명을 입력하세요',
            }
        ), label="아이디"
    )

    user_nickname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': '닉네임을 입력하세요',
            }
        ), label="닉네임"
    )
