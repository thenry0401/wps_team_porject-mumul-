from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.validators import UniqueValidator

from ..models import User

__all__ = (
    'UserSerializer',
    'UserFastCreationSerializer',
)


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

        # user = get_user_model().objects.create(
        #     email=validated_data['email'],
        #     username=validated_data['username']
        # )
        # user.set_password(validated_data['password'])
        # user.save()
        # return user

    class Meta:
        model = User
        write_only_fields = ('password', )
        read_only_fields = ('id', )
        fields = (
            'pk',
            'nickname',
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



class PaginatedUserSerializer(PageNumberPagination):
    """
    Serializes page objects of user querysets.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    class Meta:
        object_serializer_class = UserSerializer


class EverybodyCanAuthentication(SessionAuthentication):
    def authenticate(self, request):
        return None