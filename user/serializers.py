from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler


class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=6, max_length=20, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs: dict):
        if attrs.get('password') == attrs.get('password_confirm'):
            if not User.objects.filter(email=attrs.get('email')).exists():
                return attrs
            else:
                raise serializers.ValidationError('邮箱已被注册')
        else:
            raise serializers.ValidationError('两次密码输入不一致！')

    def create(self, validated_data):
        user = User.objects.create_superuser(username=validated_data['username'],
                                             email=validated_data['email'],
                                             password=validated_data['password'])
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_confirm', 'email', 'token')
        extra_kwargs = {
            'username': {
                'min_length': 6,
                'max_length': 20
            },
            'password': {
                'min_length': 6,
                'max_length': 20,
                'write_only': True
            },
            'email': {
                'required': True,
                'write_only': True
            }
        }
