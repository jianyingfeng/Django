from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import json
from .models import Projects
from django.db import connection


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


# class ProjectsView(View):
#     def get(self, request, pk):
#         # 新增，方式一：
#         # a、直接使用模型类（字段名1=值1，字段名2=值2，），来创建模型实例
#         # b、必须调用save()方法，才会执行sql语句
#         # obj = Projects(name='在线图书项目', leader='多喝热水')
#         # obj.save()
#
#         # 方式二：
#         # a、使用模型类.objects返回manager对象
#         # b、使用manager.对象.create(字段名1=值一，字段名2=值2，...)，来创建模型类实例
#         # c、无需使用模型实例调用save()方法，会自动执行sql语句
#         # obj = Projects.objects.create(name='Melu Heaven项目', leader='瑞文')
#
#         # 读取
#         # 1、读数据库全部数据
#         # a、使用模型类.ojects.all(),会将当前模型类对应的数据表中的所有数据读取出来
#         # b、模型类.objects.all()，返回QuerySet对象（查询集对象）
#         # c、QuerySet对象，类似于列表，具有惰性查询的特性（在‘用’数据时，才会执行sql语句）
#         # qs = Projects.objects.all()
#         # 2、读单条数据
#         # 方式一：
#         # a、可以使用模型类.objects.get(条件1=值1)
#         # b、匹配的记录数为0，会抛出异常
#         # c、匹配的记录数大于1，也会抛出异常
#         # d、这种查询方式适用于查询条件为唯一约束
#         # e、匹配到了唯一一条记录，可以使用模型对象.字段名去获取字段值
#         # qs = Projects.objects.get(name='你叉叉项目')
#         # pass
#
#         # 2、读单条数据
#         # 方式一：
#         # a、可以使用模型类.objects.filter(条件1=值1)，返回QuerySet对象
#         # b、匹配的记录数为0，会返回空的QuerySet对象
#         # c、匹配的记录数大于1，会返回有值的QuerySet对象
#         # d、QuerySet对象，类似于列表，有如下特性：
#         # 1）支持通过0和正索引取值
#         # 2）不支持负数索引取值
#         # 3）QuerySet对象.first()取第一个值
#         # 4）QuerySet对象.last()取最后一个值
#         # 5）len(QuerySet对象)  或者  QuerySet对象.count()获取长度
#         # 6）QuerySet对象.exists()判断对象是否为空
#         # 7）支持for循环
#         # qs = Projects.objects.filter(id=1)
#         # e、ORM框架会给每张表的主键指定一个别名，pk
#         # qs = Projects.objects.filter(pk=1)
#         # qs = Projects.objects.filter(id__gt=1)
#         # filter方法查询：
#         # 1）字段名__exact=具体值，等价于字段名=具体值
#         # 2）字段名__gt=具体值，大于、字段名__gte=具体值，大于等于
#         # 3）字段名__lt=具体值，小于、字段名__lte=具体值，小于等于
#         # 4）contains：包含
#         # 5）startswith：以xxx开头，istartswith：忽略大小写
#         # 6）endswith：以xxx结尾，iendswith：忽略大小写
#         # 7）isnull：是否为null
#         # 8）in：在什么中，可接列表
#         pass
#         # return JsonResponse(projects_data_list, json_dumps_params={'ensure_ascii': False}, safe=False)
#
#     def post(self, request, pk):
#         return HttpResponse('<h1>新增项目信息</h1>')
#
#     def put(self, request):
#         return HttpResponse('<h1>修改项目信息</h1>')
#
#     def delete(self, request):
#         return HttpResponse('<h1>删除项目信息</h1>')


class ProjectsView(View):
    # 需求：获取所有项目数据
    def get(self, request):
        # a、获取所有项目的查询集
        queryset = Projects.objects.all()
        # b、定义空列表
        projects_list = []
        # c、将查询集对象遍历出来放进空列表
        for item in queryset:
            item: Projects
            projects_list.append(
                {
                    'id': item.id,
                    'name': item.name,
                    'leader': item.leader
                }
            )
        # c、返回数据
        # safe=False，当传入参数不为字典类型时，依旧可以转换为json对象
        return JsonResponse(projects_list, safe=False)

    # 需求：创建一条数据
    def post(self, request):
        # 先获取到请求体中的参数
        try:
            python_data = json.loads(request.body)
        except:
            return JsonResponse({'msg': '参数格式有误'}, status=400)
        try:
            python_data.get('name')
        except:
            return JsonResponse({'msg': '缺少name参数'}, status=400)
        try:
            python_data.get('leader')
        except:
            return JsonResponse({'msg': '缺少leader参数'}, status=400)
        try:
            python_data.get('is_execute')
        except:
            return JsonResponse({'msg': '缺少is_execute参数'}, status=400)
        # 校验name字段类型
        if isinstance(python_data.get('name'), str):
            # 校验name字段类型长度
            if len(python_data.get('name')) <= 20:
                # 校验leader字段类型
                if isinstance(python_data.get('leader'), str):
                    # 校验leader字段类型长度
                    if len(python_data.get('leader')) <= 10:
                        # 校验is_execute字段类型
                        if isinstance(python_data.get('is_execute'), bool):
                            # 校验desc字段类型
                            if isinstance(python_data.get('desc'), str):
                                # 将请求参数写入到obj类中
                                obj = Projects.objects.create(name=python_data.get('name'),
                                                              leader=python_data.get('leader'),
                                                              is_execute=python_data.get('is_execute'),
                                                              desc=python_data.get('desc'))
                                # 返回刚刚创建好的这条数据
                                return JsonResponse({
                                    'name': obj.name,
                                    'leader': obj.leader,
                                    'msg': '创建成功'
                                })
                            else:
                                return JsonResponse({'msg': 'desc参数格式错误'}, status=400)
                        else:
                            return JsonResponse({'msg': 'is_execute参数格式错误'}, status=400)
                    else:
                        return JsonResponse({'msg': 'leader参数超出长度'}, status=400)
                else:
                    return JsonResponse({'msg': 'leader参数格式错误'}, status=400)
            else:
                return JsonResponse({'msg': 'name参数超出长度'}, status=400)
        else:
            return JsonResponse({'msg': 'name参数格式错误'}, status=400)


class ProjectsDetailView(View):
    # 需求：查询单条项目数据
    def get(self, request, pk):
        # 1、先校验数据是否存在
        # 略
        # 2、从数据中获取项目数据
        try:
            item = Projects.objects.get(id=pk)
        except:
            return JsonResponse({'msg': '参数格式有误'}, status=400)
        python_data = {
            'data': {
                'id': item.id,
                'name': item.name,
                'leader': item.leader
            },
            'msg': '获取成功'
        }
        # 3、返回数据
        return JsonResponse(python_data)

    # 更新项目信息
    def put(self, request, pk):
        # rs = request
        # pass
        python_data = json.loads(request.body)

        try:
            obj = Projects.objects.get(id=pk)
        except:
            return JsonResponse('参数格式有误', status=400, safe=False)

        obj.name = python_data.get('name')
        obj.leader = python_data.get('leader')
        obj.save(update_fields=['name', 'leader'])
        res_data = {
            'data': {
                'id': obj.id,
                'name': obj.name,
                'leader': obj.leader
            },
            'msg': '更新成功'
        }
        return JsonResponse(res_data)

    # 删除项目
    def delete(self, request, pk):
        try:
            Projects.objects.get(id=pk).delete()
        except:
            return JsonResponse('参数格式有误', status=400, safe=False)
        return JsonResponse({
            'msg': '删除成功！'
        })
