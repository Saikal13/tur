from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import RegisterSerializer, UserSerializer



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]  # ВАЖНО


class MeView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(self.serializer_class(request.user).data)
