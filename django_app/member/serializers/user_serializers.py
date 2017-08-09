from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.validators import UniqueValidator

from ..models import User

__all__ = (
    'UserSerializer',
    'UserFastCreationSerializer',
    'UserCreationSerializer',
    'PaginatedUserSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     if password is not None:
    #         instance.set_password(password)
    #     instance.save()
    #     return instance

    # user = get_user_model().objects.create(
    #     email=validated_data['email'],
    #     username=validated_data['username']
    # )
    # user.set_password(validated_data['password'])
    # user.save()
    # return user

    class Meta:
        model = User
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        fields = (
            'pk',
            'nickname',
            'name',
            'email',
            'user_type',
            'post_code', 'road_address', 'detail_address',
            'date_joined', 'last_login'
        )


class UserFastCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("중복되는 이메일이 존재합니다.")
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 서로 일치하지 않습니다.')
        return data

    def save(self, *args, **wargs):
        user = User.objects.create_user(
            email=self.validated_data.get('email', ''),
            password=self.validated_data.get('password1', ''),
        )
        return user


class UserCreationSerializer(serializers.ModelSerializer):
    """
    소셜 로그인이 아닌 일반 회원가입을 의미합니다.
    """
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())], label="이메일",
                                   style={'placeholder': "회원 이메일"})
    password1 = serializers.CharField(write_only=True, min_length=8, label="비밀번호(8자 이상)",
                                      style={'placeholder': "패스워드 입력", 'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, min_length=8, label="비밀번호 재입력(8자 이상)",
                                      style={'placeholder': "패스워드 재입력", 'input_type': 'password'})
    name = serializers.CharField(label="이름", style={'placeholder': "유저의 실명"})
    nickname = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())],
                                     label="닉네임", style={'placeholder': "사이트에서 사용할 별명"})

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'password1',
            'password2',
            'name',
            'nickname',
            'post_code', 'road_address', 'detail_address',
            'date_joined', 'last_login',
            'user_type',
        )
        write_only_fields = ('email', 'name', 'nickname', 'password1', 'password2')
        read_only_fields = ('post_code', 'road_address', 'detail_address', 'date_joined', 'last_login', 'user_type',)

    def validate_email(self, email):
        """중복되는 이메일이 있는지 검사합니다."""
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("중복되는 이메일이 존재합니다.")
        return email

    def validate_password(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('비밀번호가 서로 일치하지 않습니다.')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'],
                                        password=validated_data['password1'],
                                        name=validated_data['name'],
                                        nickname=validated_data['nickname']
                                        )
        return user


class PaginatedUserSerializer(PageNumberPagination):
    """
    Serializes page objects of user querysets.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    class Meta:
        object_serializer_class = UserSerializer
