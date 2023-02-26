"""
Views for the user API.
"""
from rest_framework import (
    generics,
    authentication,
    permissions,
    status,
)

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    ManageUserSerializer,
    ListUsersSerializer,
    UserPublicProfileSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = ManageUserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


@api_view(['GET'])
def list_all_users(request):
    users = get_user_model().objects.all().order_by('-created_on')
    serializer = ListUsersSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def user_profile_detail(request, slug):
    try:
        user = get_user_model().objects.get(
            user_name=slug,
        )
        serializer = UserPublicProfileSerializer(user)
        return Response(serializer.data)
    except get_user_model().DoesNotExist:
        return Response({}, status=status.HTTP_404_NOT_FOUND)
