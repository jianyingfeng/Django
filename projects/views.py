import logging

from django.db import connection
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Projects
from .serializers import ProjectModelSerializers, ProjectModelSerializers0120, ProjectModelSerializers0123
from interfaces.serializers import InterfacesSerializer0125

# 定义一个日志器，参数名为settings.py中定义好的日志器名称
logger = logging.getLogger('mytest')


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

    # 自定义方法不走序列化类
    # 仅获取项目id和项目名称的接口
    # 1、使用action装饰器可以给自定义action方法生成路由条目
    # 2、methods指定请求方法名称，不指定，默认为GET
    # 3、detail代表是否需要传pk值
    # 4、url_path指定url路径，默认为action方法名称
    # 5、url_name指定url路由条目名称后缀，默认为"根路由-action方法名称"
    # @action(methods=['GET'], detail=False, url_path='xxx', url_name='yyy')
    @action(methods=['GET'], detail=False)
    def names(self, request, *args, **kwargs):
        # queryset = self.get_queryset()
        # pro_list = []
        # for project in queryset:
        #     pro_list.append({
        #         'id': project.id,
        #         'name': project.name
        #     }
        #     )
        res = super().list(request, *args, **kwargs)
        # 输出日志
        logger.info(res.data)
        return res

    # 重写retrieve方法
    # 1、先调用父类的retrieve方法，返回数据
    # 2、再对上述数据进行改造
    def retrieve(self, request, *args, **kwargs):
        res = super().retrieve(request, *args, **kwargs)
        res.data.pop('id')
        res.data.pop('create_time')
        res.data.pop('update_time')
        return res

    # 需求:
    # 对names方法进行改造,需要调用list方法,但是需要替换查询集,不需要过滤,分页功能,
    # 且要有与list方法不同的序列化器类进行输出

    # 步骤1
    # 重写get_queryset方法
    # 当方法名为name时,替换查询集
    def get_queryset(self):
        if self.action == 'names':
            return self.queryset.filter(name__icontains=3)
        else:
            return super().get_queryset()

    # 步骤2
    # 重写过滤方法
    # 当方法名为name时,不作过滤
    def filter_queryset(self, queryset):
        if self.action == 'names':
            return queryset
        else:
            return super().filter_queryset(queryset)

    # 步骤3
    # 重写分页方法
    # 当方法名为name时,不作分页
    def paginate_queryset(self, queryset):
        if self.action == 'names':
            return None
        else:
            return super().paginate_queryset(queryset)

    # 步骤4
    # 重写获取序列化类的方法
    def get_serializer_class(self):
        # 获取请求方法
        if self.action == 'names':
            return ProjectModelSerializers0123
        else:
            return super().get_serializer_class()

# 类视图五大原则
# 1、类视图尽量简化
# 2、根据需求选择父类
# 3、如果父类的方法满足需求，则直接调用
# 4、如果父类的方法大部分满足需求，则重写
# 5、如果父类的方法完全不满足需求，则自定义
