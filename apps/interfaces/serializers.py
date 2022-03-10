from rest_framework import serializers

from .models import Interfaces
from projects.models import Projects


class TestcasesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class ConfiguresSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


# 给获取接口列表使用的序列化器类
class InterfacesSerializer(serializers.ModelSerializer):
    # 接口所属项目名称
    # 父表数据只有一条，不需要加many=True
    project = serializers.StringRelatedField(label='接口所属项目名称', help_text='接口所属项目名称')
    # 接口所属项目id，在创建数据的时候，前端传递的是项目id，to_internal_value方法会自动返回模型对象
    # 所以要修改create函数和update函数
    project_id = serializers.PrimaryKeyRelatedField(label='接口所属项目id', help_text='接口所属项目id',
                                                    queryset=Projects.objects.all())

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        result['project_id'] = result['project_id'].id
        return result

    # def create(self, validated_data):
    #     validated_data['project_id'] = validated_data['project_id'].id
    #     return super().create(validated_data)
    #     pass

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
class TestcasesSerializer0308(serializers.ModelSerializer):
    testcases_set = TestcasesSerializer(label='接口附属用例id、name',
                                        help_text='接口附属用例id、name',
                                        many=True, required=False)

    class Meta:
        model = Interfaces
        fields = ('testcases_set', )


class ConfiguresSerializer0308(serializers.ModelSerializer):
    configures = ConfiguresSerializer(label='接口附属配置id、name',
                                      help_text='接口附属配置id、name',
                                      many=True, required=False)

    class Meta:
        model = Interfaces
        fields = ('configures', )