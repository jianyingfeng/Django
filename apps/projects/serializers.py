from rest_framework import serializers, filters
from rest_framework.validators import UniqueValidator

from utils.pagination import PageNumberPagination
from utils.base_serializers import RunSerializer
# 导入时前面不能加apps目录，否则会报错（且此时必须将apps目录标记为Resource Root）
# from apps.debugtalks.models import DebugTalks
from debugtalks.models import DebugTalks
from .models import Projects


# 这个类不会返回更新时间
class ProjectModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Projects
        exclude = ('update_time',)
        extra_kwargs = {
            'create_time': {
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }

    def create(self, validated_data):
        instance = super().create(validated_data)
        # 在创建项目的同时，还需创建debug关联数据，其他字段在模型类中已经定义好了默认值，
        # 外键传值的写法如下：
        DebugTalks.objects.create(project=instance)
        return instance


# 这个类只会返回项目id、项目名称
class ProjectModelSerializers0123(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = ('id', 'name')


# 这个类只会返回接口id和名称
class InterfaceModelSerializers(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


# 这个类只会返回接口id和接口名称
class ProjectModelSerializers0307(serializers.ModelSerializer):
    interfaces = InterfaceModelSerializers(label='项目附属接口id及名称', help_text='项目附属接口id及名称',
                                           many=True, required=False)

    class Meta:
        model = Projects
        fields = ('interfaces',)


# 集成公共序列化器类
class ProjectsRunSerializer(RunSerializer):
    # 继承内部类的写法
    class Meta(RunSerializer.Meta):
        model = Projects
