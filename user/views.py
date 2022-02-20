from rest_framework import mixins, viewsets
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import RegisterUserSerializer, UsernameCountSerializer, EmailCountSerializer


class RegisterUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer

    @action(detail=True)
    def count_username(self, request, username, *args, **kwargs):
        count = len(User.objects.filter(username=username))
        return Response({
            'username': username,
            'count': count
        })

    @action(detail=False)
    def count_email(self, request, *args, **kwargs):
        count = len(User.objects.filter(email=request.data))
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