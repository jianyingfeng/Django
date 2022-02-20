from rest_framework import mixins, viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response

from .serializers import RegisterUserSerializer, UsernameCountSerializer, EmailCountSerializer


class RegisterUserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    def count_username(self, request, *args, **kwargs):
        count = len(User.objects.filter(name=request.data))
        data = {
            'username': request.data,
            'count': count
        }
        return Response(data)

    def count_email(self, request, *args, **kwargs):
        count = len(User.objects.filter(name=request.data))
        data = {
            'email': request.data,
            'count': count
        }
        return Response(data)

    def get_serializer_class(self):
        # 获取请求方法
        if self.action == 'count_username':
            return UsernameCountSerializer
        elif self.action == 'count_email':
            return EmailCountSerializer
        else:
            return super().get_serializer_class()