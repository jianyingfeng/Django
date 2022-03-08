from rest_framework import viewsets

from interfaces.models import Interfaces
from .serializers import InterfacesSerializer, InterfacesSerializer0308
from configures.models import Configures
from testcases.models import Testcases
from projects.models import Projects


class InterfacesViewSet(viewsets.ModelViewSet):
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesSerializer

    # 在获取接口列表的响应中添加配置数和测试用例数
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for item in response.data['results']:
            configure_num = Configures.objects.filter(interface=item['id']).count()
            testcase_num = Testcases.objects.filter(interface=item['id']).count()
            project_name = Projects.objects.get(id=item['project']).name
            # 在获取接口列表的响应中添加配置数和测试用例数
            item['configure'] = configure_num
            item['testcase'] = testcase_num
            item['project'] = project_name
        return response

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return InterfacesSerializer0308
        else:
            return super().get_serializer_class()
