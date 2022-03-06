from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=6, max_length=20, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs: dict):
        if attrs.get('password') == attrs.get('password_confirm'):
            if not User.objects.filter(email=attrs.get('email')).exists():
                attrs.pop('password_confirm')
                return attrs
            else:
                raise serializers.ValidationError('邮箱已被注册')
        else:
            raise serializers.ValidationError('两次密码输入不一致！')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        return user

    class Meta:
        model = User
        # id字段默认read_only=True,此处无需额外指定
        fields = ('id', 'username', 'password', 'password_confirm', 'email', 'token')
        extra_kwargs = {
            # username字段在模型类中指定了unique=True，所以此处不需要进行唯一性校验
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