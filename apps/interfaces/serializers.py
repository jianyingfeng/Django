from rest_framework import serializers
from .models import Interfaces


class TestcasesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class ConfiguresSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


# 给获取接口列表使用的序列化器类
class InterfacesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Interfaces
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }


# 给获取单个接口信息使用的序列化器类
# 会携带接口附属用例id、name以及接口附属配置id、name
class InterfacesSerializer0308(serializers.ModelSerializer):
    testcases_set = TestcasesSerializer(label='接口附属用例id、name',
                                        help_text='接口附属用例id、name',
                                        many=True, required=False)
    configures = ConfiguresSerializer(label='接口附属配置id、name',
                                      help_text='接口附属配置id、name',
                                      many=True, required=False)

    class Meta:
        model = Interfaces
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }
