from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import RegisterUserSerializer


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer