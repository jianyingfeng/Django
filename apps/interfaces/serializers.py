from rest_framework import serializers

from .models import Interfaces
from projects.models import Projects
from utils.base_serializers import RunSerializer


class TestcasesSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class ConfiguresSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


# 需求：
# 获取接口列表时需要返回项目id、项目名称
# 创建、更新接口时仅需要传递项目id
class InterfacesSerializer(serializers.ModelSerializer):
    # 接口所属项目名称
    # 父表数据只有一条，不需要加many=True
    # 自动指定了read_only = True, 该字段仅格式化输出
    project = serializers.StringRelatedField(label='接口所属项目名称', help_text='接口所属项目名称')
    # 接口所属项目id，在创建数据的时候，前端传递的是项目id，PrimaryKeyRelatedField类中to_internal_value方法会自动返回模型对象
    # 所以要修改create方法和update方法，都改太麻烦，就改to_internal_value方法，从而实现在
    # 调用create方法和update方法之前对数据进行修改
    project_id = serializers.PrimaryKeyRelatedField(label='接口所属项目id', help_text='接口所属项目id',
                                                    queryset=Projects.objects.all())

    class Meta:
        model = Interfaces
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        # 方式一：
        # result的project_id字段值是一个project模型对象，需要替换成project的id
        # result['project_id'] = result['project_id'].id

        # 方式二：
        # 将project模型对象赋值给project字段，并将project_id删除
        result['project'] = result.pop('project_id')
        return result

    # def create(self, validated_data):
    #     validated_data['project_id'] = validated_data['project_id'].id
    #     return super().create(validated_data)
    #     pass


# 给获取单个接口信息使用的序列化器类
# 会携带接口附属用例id、name以及接口附属配置id、name
class TestcasesSerializer0308(serializers.ModelSerializer):
    testcases_set = TestcasesSerializer(label='接口附属用例id、name',
                                        help_text='接口附属用例id、name',
                                        many=True, required=False)

    class Meta:
        model = Interfaces
        fields = ('testcases_set',)


class ConfiguresSerializer0308(serializers.ModelSerializer):
    configures = ConfiguresSerializer(label='接口附属配置id、name',
                                      help_text='接口附属配置id、name',
                                      many=True, required=False)

    class Meta:
        model = Interfaces
        fields = ('configures',)


class InterfaceRunSerializer(RunSerializer):
    class Meta(RunSerializer.Meta):
        model = Interfaces
