import re, json

from rest_framework import serializers
from utils.base_serializers import RunSerializer
from rest_framework.validators import UniqueValidator
from utils.pagination import PageNumberPagination

from testsuites.models import Testsuites
from projects.models import Projects
from interfaces.models import Interfaces


# 获取testsuite列表使用的序列化器类
class TestsuiteModelSerializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称')
    project_id = serializers.PrimaryKeyRelatedField(label='所属项目id', help_text='所属项目id',
                                                    queryset=Projects.objects.all())

    class Meta:
        model = Testsuites
        fields = '__all__'
        extra_kwargs = {
            'include': {
                'write_only': True
            },
            'create_time': {
                'format': '%Y-%m-%d %H:%M:%S'
            },
            'update_time': {
                'format': '%Y-%m-%d %H:%M:%S'
            }
        }

    # 此处与interface模块逻辑一致，可以抽象到utils当中
    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        result['project_id'] = result.pop('project_id').id
        return result

    # 对include字段进行校验
    # 1、先进行正则匹配
    # 2、对列表中的接口id进行去重
    # 3、对列表中的每个接口id进行校验
    def validate_include(self, attr):
        # 正则表达式
        # ^:以什么开头
        # $:以什么结尾
        # \[：将[转义
        # \]：将]转义
        # \d:匹配数字0-9
        # +:匹配一次或多次
        # *：匹配0次或多次
        result = re.match(r'^\[\d+( *, *\d+)*\]$', attr)
        if result is None:
            raise serializers.ValidationError('include参数不合法')
        result = result.group()
        data = json.loads(result)
        include_list_new = []
        for i in data:
            if i not in include_list_new:
                include_list_new.append(i)
        for item in include_list_new:
            if not Interfaces.objects.filter(id=item).exists():
                raise serializers.ValidationError(f'接口id:{item}不存在')
        return include_list_new

    # 对include字段进行校验
    # 1、先转成列表
    # 2、将接口id装换为整数
    # 3、对列表中的接口id进行去重
    # 4、对列表中的每个接口id进行校验
    # def validate_include(self, attr):
    #     try:
    #         include_list = eval(attr)
    #     except:
    #         raise serializers.ValidationError('include参数不合法')
    #     if not isinstance(include_list, list):
    #         raise serializers.ValidationError('include不是数组')
    #     include_list_new = []
    #     for i in include_list:
    #         try:
    #             isinstance(int(i), int)
    #             i_new = int(i)
    #         except:
    #             raise serializers.ValidationError(f'接口id:{i}须为整数')
    #         if i_new not in include_list_new:
    #             include_list_new.append(i_new)
    #     for item in include_list_new:
    #         try:
    #             Interfaces.objects.get(id=item)
    #         except:
    #             raise serializers.ValidationError(f'接口id:{item}不存在')
    #     return include_list_new


class TestsuiteRunSerializer(RunSerializer):
    class Meta(RunSerializer.Meta):
        model = Testsuites
