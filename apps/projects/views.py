import logging

from django.db import connection
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, Count, Avg, Max, Min

from .models import Projects
from .serializers import ProjectModelSerializers, ProjectModelSerializers0123, ProjectModelSerializers0307
from interfaces.models import Interfaces
from testsuites.models import Testsuites
from testcases.models import Testcases
from configures.models import Configures

# from interfaces.serializers import InterfacesSerializer0125

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
    # 在视图类中指定认证方式，优先级高于全局认证方式
    # 一个项目一般都是统一的认证方式，无须额外在视图类中指定
    # authentication_classes = []
    # 在视图类中指定权限类，优先级高于全局
    permission_classes = [permissions.IsAuthenticated]
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

    # 需求：获取项目列表，且要获取与项目相关联的interfaces、testsuites、testcases、configures数量
    # 项目是与且要获取与项目相关联的interfaces、testsuites相关联，
    # testcases、configures与且要获取与项目相关联的interfaces相关联
    def list(self, request, *args, **kwargs):
        # 1、调用父类的list方法获取项目列表
        response = super().list(request, *args, **kwargs)
        for item in response.data['results']:
            # 2、获取单个项目下的接口的查询集
            interfaces_qs = Interfaces.objects.filter(project=item['id'])
            # 3、获取单个项目下的接口的数量
            interfaces_num = interfaces_qs.count()
            # 4、获取单个项目下的套件的数量
            testsuites_num = Testsuites.objects.filter(project=item['id']).count()

            # # 获取测试用例数量、测试配置数量的方法一：
            # # 定义一个空列表，用来存储单个项目下的接口id
            # interfaces_id_list = []
            # for i in range(0, len(interfaces_qs)):
            #     interfaces_id_list.append(interfaces_qs[i].id)
            # # 5、利用分组查询获取interfaces_id_list中各个接口id所关联的测试用例数量
            # testcases_num = Testcases.objects.filter(interface__in=interfaces_id_list).count()
            # # 6、利用分组查询获取interfaces_id_list中各个接口id所关联的测试配置数量
            # configures_num = Configures.objects.filter(interface__in=interfaces_id_list).count()

            # 获取测试用例数量、测试配置数量的方法二：
            # 通过关联字段查询项目下关联的测试用例数量、测试配置数量
            testcases_num = Testcases.objects.filter(interface__project__id=item['id']).count()
            configures_num = Configures.objects.filter(interface__project__id=item['id']).count()
            # 7、将各个数量添加到响应中
            item['interfaces'] = interfaces_num
            item['testsuits'] = testsuites_num
            item['testcases'] = testcases_num
            item['configures'] = configures_num
        return response

    # 获取项目下接口id和名称
    # 通过替换序列化器类来实现
    @action(methods=['GET'], detail=True)
    def interfaces(self, request, *args, **kwargs):
        project_obj = super().retrieve(request, *args, **kwargs)
        response = project_obj.data['interfaces']
        return Response(response)

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
        # res.data.pop('update_time')
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
        elif self.action == 'interfaces':
            return ProjectModelSerializers0307
        else:
            return super().get_serializer_class()

# 类视图五大原则
# 1、类视图尽量简化
# 2、根据需求选择父类
# 3、如果父类的方法满足需求，则直接调用
# 4、如果父类的方法大部分满足需求，则重写
# 5、如果父类的方法完全不满足需求，则自定义

# 视图类方法的总结：
# 1、视图类继承了ModelViewSet，则拥有增删改查6个接口
# 2、上述6个接口可以用现成的，如不满足需求可以进行改造
# 改造原则：
# 2.1、如果是对自身模型类进行字段的增、删，则去改造序列化器类
# 2.2、如果需要查询到关联表的字段值，则通过自定义序列化器类，将关联表的字段进行序列化输出
# 2.3、如果涉及到关联表的聚合运算，则直接在action方法中进行聚合运算，再将结果添加到响应中
# 2.4、创建关联表数据，则改造序列化器类中的create方法
