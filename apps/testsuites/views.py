import os
import json
from datetime import datetime

from rest_framework import viewsets
from rest_framework.decorators import action
from django.conf import settings

from testsuites.models import Testsuites
from testcases.models import Testcases
from envs.models import Envs
from testsuites.serializers import TestsuiteModelSerializer, TestsuiteRunSerializer
from utils import common
from utils.mixins import RunMixin


class TestsuiteViewSet(RunMixin, viewsets.ModelViewSet):
    serializer_class = TestsuiteModelSerializer
    queryset = Testsuites.objects.all()

    # 运行单个测试套件下所有用例方式一
    # @action(methods=['POST'], detail=True)
    # def run(self, request, *args, **kwargs):
    #     # 获取测试套件模型对象
    #     instance = self.get_object()
    #     # 获取env_id
    #     serializer = self.get_serializer(data=request.data)
    #     # 校验通过返回True，不通过则返回报错信息
    #     serializer.is_valid(raise_exception=True)
    #     env_id = serializer.validated_data.get('env_id')
    #     env = Envs.objects.get(id=env_id)
    #     # 创建时间戳目录
    #     testcase_dir_path = os.path.join(settings.PROJECT_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
    #     os.makedirs(testcase_dir_path)
    #     # 获取套件包含的接口
    #     interfaces_id_list = json.loads(instance.include)
    #     # 获取接口下的用例
    #     for interface_id in interfaces_id_list:
    #         testcase_qs = Testcases.objects.filter(interface_id=interface_id)
    #         for testcase_obj in testcase_qs:
    #             # 创建以项目名命名的目录
    #             # 创建以debugtalk.py，yaml文件
    #             common.generate_testcase_file(testcase_obj, env, testcase_dir_path)
    #     # 运行用例并生成测试报告
    #     return common.run(instance, testcase_dir_path)

    # 运行单个测试套件下所有用例优化
    @action(methods=['POST'], detail=True)
    def run(self, request, *args, **kwargs):
        instance = self.get_object()
        # 获取套件包含的接口id
        interfaces_id_list = json.loads(instance.include)
        # 获取接口下的用例
        for interface_id in interfaces_id_list:
            # 获取用例查询集
            testcase_qs = Testcases.objects.filter(interface_id=interface_id)
            return self.execute(instance, testcase_qs, request)

    def get_serializer_class(self):
        if self.action == 'run':
            return TestsuiteRunSerializer
        else:
            return super().get_serializer_class()
