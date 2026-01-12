from django.contrib.auth.models import User

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import ChangePasswordSerializer, UserProfileSerializer, UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    POST /api/users/register/
    Registra un nuevo usuario.
    """

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /api/users/profile/ - Ver perfil
    PUT/PATCH /api/users/profile/ - Actualizar perfil
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        """
        Retorna el usuario autenticado.
        """
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    """
    PUT /api/users/change-password/
    Cambia la contraseña del usuario.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        """
        Retorna el usuario autenticado.
        """
        return self.request.user

    def update(self, request, *args, **kwargs):
        """
        Actualiza la contraseña.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Contraseña actualizada correctamente."},
            status=status.HTTP_200_OK,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    GET /api/users/me/
    Retorna información del usuario actual.
    """
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)
