from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Projects
from .serializers import ProjectModelSerializers, ProjectModelSerializers111


# a、可以继承视图集类ModelViewSet
# b、在定义url路由条目时，支持给as_view传递字典参数（请求方法名与具体的action方法名的一一对应关系）
# c、ModelViewSet继承了CreateModelMixin、RetrieveModelMixin、UpdateModelMixin、
# DestroyModelMixin、ListModelMixin、GenericViewSet，
# 前面的父类提供了action方法、GenericViewSet提供了get_queryset、get_serializer、get_object方法
# d、具备APIView的所有功能
# e、ModelViewSet继承了GenericViewSet，又从上继承了ViewSetMixin，所以具有功能：
# 在定义url路由条目时，支持给as_view传递字典参数（请求方法名与具体的action方法名
class ProjectsViewSet(viewsets.ModelViewSet):
    # 这里会在接口平台上展示每个请求方法下的注释，冒号是英文冒号
    """
    list:
    获取项目列表数据

    create:
    创建项目

    interfaces:
    获取项目附属接口数据
    """
    queryset = Projects.objects.all()
    serializer_class = ProjectModelSerializers
    """
    action方法：
    get：list-->获取列表数据
    get：retrieve-->获取详情数据
    post：create-->创建数据
    put：update-->更新数据（完整）
    patch：partial_update-->更新数据（部分）
    delete:destroy-->删除数据
    """

    # 自定义方法不走序列化类
    # 仅获取项目id和项目名称的接口
    # 1、使用action装饰器可以给自定义action方法生成路由条目
    # 2、methods指定请求方法名称，不指定，默认为GET
    # 3、detail代表是否需要传pk值
    # 4、url_path指定url路径，默认为action方法名称
    # 5、url_name指定url路由条目名称后缀，默认为"根路由-action方法名称"
    @action(methods=['GET'], detail=False, url_path='xxx', url_name='yyy')
    def names(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        pro_list = []
        for project in queryset:
            pro_list.append({
                'id': project.id,
                'name': project.name
            }
            )
            # pro_list.append(project)
        return Response(pro_list)

    # 自定义方法不走序列化类
    # 获取项目下接口信息的接口
    @action(methods=['GET'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        obj = self.get_object()
        queryset = obj.interfaces_set.all()
        inter_list = []
        for interface in queryset:
            inter_list.append({
                'id': interface.id,
                'name': interface.name
            })
        return Response(inter_list)

    # 重写获取序列化类的方法
    def get_serializer_class(self):
        # 获取请求方法
        if self.action == 'retrieve':
            return ProjectModelSerializers111
        else:
            return super().get_serializer_class()