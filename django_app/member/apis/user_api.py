from rest_framework import generics, serializers

from member.serializers import UserSerializer
from member.serializers.user_serializers import UserCreationSerializer
from ..models import User

__all__ = (
    'UserListCreateView',

)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        elif self.request.method == 'POST':
            return UserCreationSerializer