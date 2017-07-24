from rest_auth.serializers import LoginSerializer
from rest_framework import serializers

from ..models import User

__all__ = (
    'UserSerializer',
    'UserCreationSerializer',
    'UserLoginSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'email',
            'user_type',
        )


class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=50,
    )
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("중복되는 아이디가 존재합니다.")
        return username

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 서로 일치하지 않습니다.')
        return data

    def save(self, *args, **wargs):
        user = User.objects.create_user(
            username=self.validated_data.get('username', ''),
            password=self.validated_data.get('password1', ''),
        )
        return user


class UserLoginSerializer(LoginSerializer):
    """장고 자체 회원가입 유저의 Login Serializer"""

    # rest-auth 내 LoginSerializer에서 일반 로그인은 email 필드를 제거
    def get_fields(self):
        fields = super(LoginSerializer, self).get_fields()
        del fields['email']
        return fields
