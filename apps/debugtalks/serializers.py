from rest_framework import serializers, filters
from rest_framework.validators import UniqueValidator
from utils.pagination import PageNumberPagination

from debugtalks.models import DebugTalks


# 获取列debugtalk列表使用的序列化器类
class DebugTalksModelSerializer(serializers.ModelSerializer):
    # project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project = serializers.SlugRelatedField(label='所属项目名称', help_text='所属项目名称',
                                           slug_field='name', read_only=True)

    class Meta:
        model = DebugTalks
        fields = ('id', 'name', 'project')


# 更新，获取详情的序列化器类
class DebugTalksModelSerializer_One(serializers.ModelSerializer):
    class Meta:
        model = DebugTalks
        fields = ('id', 'debugtalk',)
