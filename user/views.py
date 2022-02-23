from rest_framework import mixins, viewsets, generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import RegisterUserSerializer


class RegisterUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    这个视图类支持一个新增方法，以及下面的两个自定义方法
    """
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    # 下面这两个方法不需要使用序列化器类（当响应数据是从数据库查询出来时，才需要使用序列化器类）
    def count_username(self, request, username, *args, **kwargs):
        count = len(User.objects.filter(username=username))
        return Response({
            'username': username,
            'count': count
        })

    def count_email(self, request, email, *args, **kwargs):
        count = len(User.objects.filter(email=email))
        return Response({
            'email': email,
            'count': count
        })