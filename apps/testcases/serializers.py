import re
import json

from rest_framework import serializers, filters
from rest_framework.validators import UniqueValidator
from utils.pagination import PageNumberPagination
from utils.validator import IsIdExists
from utils.base_serializers import RunSerializer

from testcases.models import Testcases
from interfaces.models import Interfaces
from projects.models import Projects
from configures.models import Configures


# 获取项目、接口信息的序列化器类
class I_P_Serializer(serializers.ModelSerializer):
    project = serializers.StringRelatedField(label='所属项目名称', help_text='所属项目名称',
                                             read_only=True)
    # IsIdExists('project')：调用实例会直接匹配到类中的__call__方法
    # 因为validators列表中只要写方法名，所以IsIdExists('project')不需要加()
    pid = serializers.IntegerField(label='所属项目id', help_text='所属项目id',
                                   validators=[IsIdExists('project')], write_only=True)
    iid = serializers.IntegerField(label='所属接口id', help_text='所属接口id',
                                   validators=[IsIdExists('interface')], write_only=True)

    class Meta:
        model = Interfaces
        fields = ('name', 'project', 'pid', 'iid')
        extra_kwargs = {
            'name': {
                'read_only': True
            }
        }

    # pid和iid的校验提取到了utils当中
    # 校验pid
    # def validate_pid(self, attr):
    #     if not Projects.objects.filter(id=attr).exists():
    #         raise serializers.ValidationError(f'pid：{attr}不存在')
    #     return attr

    # 校验iid
    # def validate_iid(self, attr):
    #     if not Interfaces.objects.get(id=attr):
    #         raise serializers.ValidationError(f'iid：{attr}不存在')
    #     return attr

    # 校验iid是否属于pid
    def validate(self, attrs: dict):
        pid = attrs.get('pid')
        iid = attrs.get('iid')
        if not Interfaces.objects.filter(id=iid, project_id=pid).exists():
            raise serializers.ValidationError(f'pid：{pid}下没有iid：{iid}')
        return attrs


class TestcasesSerializer(serializers.ModelSerializer):
    interface = I_P_Serializer(label='用例所属接口名称，项目名称',
                               help_text='用例所属接口名称，项目名称')

    class Meta:
        model = Testcases
        fields = ('id', 'name', 'interface', 'include', 'author', 'request')
        extra_kwargs = {
            'include': {
                'write_only': True
            },
            'request': {
                'write_only': True
            },
        }

    def validate_include(self, attr):
        if attr is None:
            pass
        else:
            try:
                attr = json.loads(attr)
            except:
                raise serializers.ValidationError('include参数格式有误')
            config = attr.get('config')
            testcases_list = attr.get('testcases')
            if config is None:
                pass
            else:
                if not Configures.objects.filter(id=config).exists():
                    raise serializers.ValidationError(f'config id：{config}不存在')
            testcases_list_new = []
            for i in testcases_list:
                if i not in testcases_list_new:
                    testcases_list_new.append(i)
            for item in testcases_list_new:
                if not Testcases.objects.filter(id=item).exists():
                    raise serializers.ValidationError(f'testcase id：{item}不存在')
        attr['testcases'] = testcases_list_new
        return attr

    # 创建和更新数据的时候需要将前端传递的参数进行改造
    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        result['interface_id'] = result.pop('interface').get('iid')
        return result


# 集成公共序列化器类
class TestcasesRunSerializer(RunSerializer):
    # 继承内部类的写法
    class Meta(RunSerializer.Meta):
        model = Testcases


# class TestcasesRunSerializer(serializers.ModelSerializer):
#     env_id = serializers.IntegerField(label='接口关联的环境配置id', help_text='接口关联的环境配置id',
#                                       validators=[IsIdExists('env')])
#
#     class Meta:
#         model = Testcases
#         fields = ('id', 'env_id')
#         extra_kwargs = {
#             'env_id': {
#                 'write_only': True
#             }
#         }
