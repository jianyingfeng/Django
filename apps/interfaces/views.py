import os
from datetime import datetime

from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from interfaces.models import Interfaces
from .serializers import InterfacesSerializer, TestcasesSerializer0308, \
    ConfiguresSerializer0308, InterfaceRunSerializer
from configures.models import Configures
from testcases.models import Testcases
from envs.models import Envs
from utils import common


class InterfacesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesSerializer

    # 在获取接口列表的响应中添加配置数和测试用例数
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for item in response.data['results']:
            configure_num = Configures.objects.filter(interface=item['id']).count()
            testcase_num = Testcases.objects.filter(interface=item['id']).count()
            # 在获取接口列表的响应中添加配置数和测试用例数
            item['configure'] = configure_num
            item['testcase'] = testcase_num
        return response

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     for item in response.data['results']:
    #         configure_num = Configures.objects.filter(interface=item['id']).count()
    #         testcase_num = Testcases.objects.filter(interface=item['id']).count()
    #         project_name = Projects.objects.get(id=item['project']).name
    #         # 在获取接口列表的响应中添加配置数和测试用例数
    #         item['configure'] = configure_num
    #         item['testcase'] = testcase_num
    #         item['project_id'] = item['project']
    #         item['project'] = project_name
    #     return response

    # 获取接口下的测试用例id和名称
    @action(methods=['GET'], detail=True)
    def testcases(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs).data['testcases_set']
        return Response(response)

    # 获取接口下的测试配置id和名称
    @action(methods=['GET'], detail=True)
    def configs(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs).data['configures']
        return Response(response)

    # 运行单个接口下所有用例
    @action(methods=['POST'], detail=True)
    def run(self, request, *args, **kwargs):
        # 获取接口模型对象
        instance = self.get_object()
        # 获取env_id
        serializer = self.get_serializer(data=request.data)
        # 校验通过返回True，不通过则返回报错信息
        serializer.is_valid(raise_exception=True)
        env_id = serializer.validated_data.get('env_id')
        env = Envs.objects.get(id=env_id)
        # 创建时间戳目录
        testcase_dir_path = os.path.join(settings.PROJECT_DIR, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        os.makedirs(testcase_dir_path)
        # 获取接口下的所用用例
        testcase_qs = Testcases.objects.filter(interface=instance)
        if len(testcase_qs) == 0:
            return Response({'msg': '此接口下没有用例！'})
        for testcase_obj in testcase_qs:
            # 创建以项目名命名的目录
            # 创建以debugtalk.py，yaml文件
            common.generate_testcase_file(testcase_obj, env, testcase_dir_path)
        # 运行用例并生成测试报告
        return common.run(instance, testcase_dir_path)

    def get_serializer_class(self):
        if self.action == 'testcases':
            return TestcasesSerializer0308
        elif self.action == 'configs':
            return ConfiguresSerializer0308
        elif self.action == 'run':
            return InterfaceRunSerializer
        else:
            return super().get_serializer_class()
