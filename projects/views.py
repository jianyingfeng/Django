from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import json
from .models import Projects
from django.db import connection


# Create your views here.


# def index(request):
#     return HttpResponse('欢迎来到德莱联盟！')
#
#
# def create_project(request):
#     return HttpResponse('创建项目信息')
#
#
# def put_project(request):
#     return HttpResponse('更新项目信息')
#
#
# def get_project(request):
#     return HttpResponse('获取项目信息')
#
#
# def delete_project(request):
#     return HttpResponse('删除项目信息')
#
#
# def get_project_by_id(request, pk):
#     return HttpResponse(f'这是项目{pk}的信息')


# def projects(request):
#     # print(request)
#     # print(type(request))
#     # print(type(request).__mro__)
#     if request.method == 'GET':
#         return HttpResponse('<h1>获取项目信息</h1>')
#     elif request.method == 'POST':
#         return HttpResponse('<h1>新增项目信息</h1>')
#     elif request.method == 'PUT':
#         return HttpResponse('<h1>修改项目信息</h1>')
#     elif request.method == 'DELETE':
#         return HttpResponse('<h1>删除项目信息</h1>')
#     else:
#         return HttpResponse('<h1>其他操作</h1>')


class ProjectsView(View):
    def get(self, request, pk):
        # 新增，方式一：
        # a、直接使用模型类（字段名1=值1，字段名2=值2，），来创建模型实例
        # b、必须调用save()方法，才会执行sql语句
        # obj = Projects(name='在线图书项目', leader='多喝热水')
        # obj.save()

        # 方式二：
        # a、使用模型类.objects返回manager对象
        # b、使用manager.对象.create(字段名1=值一，字段名2=值2，...)，来创建模型类实例
        # c、无需使用模型实例调用save()方法，会自动执行sql语句
        # obj = Projects.objects.create(name='哈赛开项目', leader='瑞文')

        # 读取
        # 1、读数据库全部数据
        # a、使用模型类.ojects.all(),会将当前模型类对应的数据表中的所有数据读取出来
        # b、模型类.objects.all()，返回QuerySet对象（查询集对象）
        # c、QuerySet对象，类似于列表，具有惰性查询的特性（在‘用’数据时，才会执行sql语句）
        # qs = Projects.objects.all()
        # 2、读单条数据
        # 方式一：
        # a、可以使用模型类.objects.get(条件1=值1)
        # b、匹配的记录数为0，会抛出异常
        # c、匹配的记录数大于1，也会抛出异常
        # d、这种查询方式适用于查询条件为唯一约束
        # e、匹配到了唯一一条记录，可以使用模型对象.字段名去获取字段值
        # qs = Projects.objects.get(name='你叉叉项目')
        # pass

        # 2、读单条数据
        # 方式一：
        # a、可以使用模型类.objects.filter(条件1=值1)，返回QuerySet对象
        # b、匹配的记录数为0，会返回空的QuerySet对象
        # c、匹配的记录数大于1，会返回有值的QuerySet对象
        # d、QuerySet对象，类似于列表，有如下特性：
        # 1）支持通过0和正索引取值
        # 2）不支持负数索引取值
        # 3）QuerySet对象.first()取第一个值
        # 4）QuerySet对象.last()取最后一个值
        # 5）len(QuerySet对象)  或者  QuerySet对象.count()获取长度
        # 6）QuerySet对象.exists()判断对象是否为空
        # 7）支持for循环
        # qs = Projects.objects.filter(id=1)
        # e、ORM框架会给每张表的主键指定一个别名，pk
        # qs = Projects.objects.filter(pk=1)
        qs = Projects.objects.filter(id__gt=1)
        # filter方法查询：
        # 1）字段名__exact=具体值，等价于字段名=具体值
        # 2）字段名__gt=具体值，大于、字段名__gte=具体值，大于等于
        # 3）字段名__lt=具体值，小于、字段名__lte=具体值，小于等于
        # 4）contains：包含
        # 5）startswith：以xxx开头，istartswith：忽略大小写
        # 6）endswith：以xxx结尾，iendswith：忽略大小写
        # 7）isnull：是否为null
        # 8）in：在什么中，可接列表
        pass
        # return JsonResponse(projects_data_list, json_dumps_params={'ensure_ascii': False}, safe=False)

    def post(self, request, pk):
        return HttpResponse('<h1>新增项目信息</h1>')

    def put(self, request):
        return HttpResponse('<h1>修改项目信息</h1>')

    def delete(self, request):
        return HttpResponse('<h1>删除项目信息</h1>')
