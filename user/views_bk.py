from rest_framework import mixins, viewsets, generics
from django.contrib.auth.models import User
from rest_framework.response import Response

from .serializers import RegisterUserSerializer, UsernameCountSerializer, EmailCountSerializer


class RegisterUserView(generics.CreateAPIView):
    """
    这个视图类仅支持创建用户的方法、以及下面两个自定义的方法
    """
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