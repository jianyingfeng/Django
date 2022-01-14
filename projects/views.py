import json

from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Projects
from .serializers import ProjectSerializers, ProjectModelSerializers


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


# class ProjectsView(View):
class ProjectsView(APIView):
    # APIView是django中View的子类
    # 需求：获取所有项目数据
    def get(self, request):
        # a、获取所有项目的查询集
        queryset = Projects.objects.all()
        # b、返回数据
        # safe=False，当传入参数不为字典类型时，依旧可以转换为json对象
        # 序列化对象，传字典时不需要many参数，传列表时需要many=True
        serializer = ProjectSerializers(instance=queryset, many=True)
        # 通过.data属性，将数据返回
        # return JsonResponse(serializer.data, safe=True)
        # 在DRF中Response为HTTPResponse的子类
        # a、会自动根据渲染器来将数据转换为请求头中Accept需要的格式进行返回
        return Response(serializer.data)

    # 需求：创建一条数据
    def post(self, request):
        # 先获取到请求体中的参数
        # try:
        #     python_data = json.loads(request.body)
        # except:
        #     return JsonResponse({'msg': '参数格式有误'}, status=400)
        # 反序列化操作
        # 通过给序列化类的data参数传参，调用is_valid()方法来对数据进行校验，通过返回True，不通过则返回False
        # 调用.errors可以返回校验未通过的提示信息，也可以通过is_valid(raise_exception=True)直接返回
        # 调用.validated_data可以返回校验通过的数据，与json.loads()转换的参数不一定一样

        # a、继承APIView之后，request是DRF中Request对象
        # b、可以使用.get、.query_params获取url中查询参数
        # c、对于前端传递的application/json、application/x-www-form-urlencoded、form-data参数，都可以使用.data来获取
        serializer = ProjectModelSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        # obj = Projects.objects.create(**revers_ser.validated_data)
        # 1、在创建序列化对象的时候，仅传递了data参数，可以调用save方法，即会调用序列化类中的create方法
        # 2、create方法中的validated_data为校验通过的参数（一般为字典）
        # 3、save方法可以传递关键字参数，会自带添加到validated_data字典中去，如果传递了模型类中的参数，则会进行覆盖
        # 4、create方法需要将创建好的模型类对象返回
        serializer.save(my_name='珍惜', my_age=28)
        # p_ser = ProjectSerializers(obj)
        # 返回刚刚创建好的这条数据
        # return JsonResponse(p_ser.data)
        # 1、可以使用创建序列化器对象.data属性，来获取序列化输出的数据，需要在is_valid方法之后使用
        # 2、如果没有调用save方法，会把validated_data当做输入源，参照序列化类的序列化字段来进行输出
        # 3、如果调用了save方法，则会将create方法返回的模型对象当做输入源，参照序列化类的序列化字段来进行输出
        # return JsonResponse(serializer.data, safe=False)
        return Response(serializer.data, safe=False)


class ProjectsDetailView(APIView):
    # 查询单条项目数据的方法
    def get_object(self, id):
        try:
            project_obj = Projects.objects.get(id=id)
            return project_obj
        except:
            return Response({'msg': '参数格式有误'}, status=400)

    # 需求：查询单条项目数据
    def get(self, request, pk):
        # 1、先校验数据是否存在
        # 略
        # 2、从数据库中获取项目数据
        # try:
        #     project_obj = Projects.objects.get(id=pk)
        # except:
        #     return Response({'msg': '参数格式有误'}, status=400)
        # 查询单条项目数据
        project_obj = self.get_object(pk)
        serializer = ProjectSerializers(project_obj)
        # 3、返回数据
        return Response(serializer.data)

    # 更新项目信息
    def put(self, request, pk):
        # 查询单条项目数据
        project_obj = self.get_object(pk)
        serializer = ProjectSerializers(instance=project_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        # project_obj.name = serializer.validated_data.get('name')
        # project_obj.leader = serializer.validated_data.get('leader')
        # project_obj.save(update_fields=['name', 'leader'])
        # 1、在创建序列化实例时，同时传了instance、data参数，在调用save方法时，会自动调用序列化类中的update方法
        # 2、update方法的instance参数是模型对象，validated_data是校验通过的数据（是一个字典）
        # 3、save方法可以传递关键字参数，会自带添加到validated_data字典中去，如果传递了模型类中的参数，则会进行覆盖
        # 4、update方法需要将更新后的模型类对象返回
        serializer.save()
        # p_ser = ProjectSerializers(instance=obj)
        # 将数据返回
        # return JsonResponse(p_ser.data)
        return Response(serializer.data)

    # 删除项目
    def delete(self, request, pk):
        try:
            Projects.objects.get(id=pk).delete()
        except:
            return Response('参数格式有误', status=400, safe=False)
        return Response({
            'msg': '删除成功！'
        })