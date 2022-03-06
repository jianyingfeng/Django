from rest_framework import serializers, filters
from rest_framework.validators import UniqueValidator

from utils.pagination import PageNumberPagination
# 导入时前面不能加apps目录，否则会报错（且此时必须将apps目录标记为Resource Root）
# from apps.debugtalks.models import DebugTalks
from debugtalks.models import DebugTalks
from .models import Projects


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