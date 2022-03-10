from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from interfaces.models import Interfaces
from .serializers import InterfacesSerializer, TestcasesSerializer0308, ConfiguresSerializer0308
from configures.models import Configures
from testcases.models import Testcases
from projects.models import Projects


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

    def get_serializer_class(self):
        if self.action == 'testcases':
            return TestcasesSerializer0308
        elif self.action == 'configs':
            return ConfiguresSerializer0308
        else:
            return super().get_serializer_class()