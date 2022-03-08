from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.db import connection
from django.db.models import Q, Count, Avg, Max, Min

from .serializers import InterfacesSerializer
from .models import Interfaces
from projects.models import Projects


# class InterfacesView(View):
#     def get(self, request):
#         # 创建从表数据，外键如何传值？
#         # 方式一：
#         # 1）获取父表模型对象
#         # 2）从表外键字段传参为父表模型对象
#         # projects_obj = Projects.objects.get(name='在线图书项目')
#         # interfaces_obj = Interfaces.objects.create(name='在线图书项目-注册接口',tester='李莫愁',projects=projects_obj)
#         # 方式二：
#         # 1）获取父表模型对象，再获取模型对象的id
#         # 2）从表外键字段_id，传参为父表模型对象的id
#         # projects_obj = Projects.objects.get(name='在线图书项目')
#         # interfaces_obj = Interfaces.objects.create(name='在线图书项目-订单接口', tester='李莫愁', projects_id=projects_obj.id)
#         # 查询接口名称包含‘登录’的项目数据
#         # 1）先按条件取到接口表数据，再通过外键属性查询父表数据
#         # Interfaces.objects.filter(name__contains='登录').first().projects
#         # 查询项目负责人包含‘热水’的接口数据
#         # 方式一：从子表查到父表
#         # Interfaces.objects.filter(projects__leader__contains='热水')
#         # 方式二：
#         # 从父表查到字表
#         # Projects.objects.filter(leader__contains='热水').first().interfaces_set.all()
#
#         # 注：get()返回的是模型对象（即一条数据），filter()返回的是QuerSet对象（即数据集）
#         # 关联查询：
#         # 根据父表参数查询子表数据
#         # Interfaces.objects.filter(projects__name__contains='在线')
#         # 根据字表参数查询父表数据
#         # Projects.objects.filter(interfaces__name__contains='登录')
#
#         # 且查询、或查询：
#         # Projects.objects.filter(name__contains='叉叉', leader__contains='水')
#         # Projects.objects.filter(name__contains='叉叉').filter(leader__contains='水')
#         # Projects.objects.filter(Q(name__contains='叉叉') | Q(leader__contains='水'))
#         # Projects.objects.filter(Q(name__contains='叉叉') & Q(leader__contains='水'))
#
#         # 排序
#         # 字段名前加“-”代表降序排列，下面表示先按id降序排，再按name升序排
#         # Projects.objects.all().order_by('-id', 'name')
#
#         # 更新
#         # 单条更新
#         # projects_obj = Projects.objects.get(id=5)
#         # projects_obj.name = '诺克萨斯项目xxx'
#         # projects_obj.desc = '春江水'
#         # 全量更新，未指定的字段也会更新（更新时间字段也会被更新）
#         # projects_obj.save()
#         # 仅更新指定的字段值
#         # projects_obj.save(update_fields=['name','desc'])
#         # 批量更新
#         # Projects.objects.filter(name__contains='叉叉').update(leader='憨xx批',desc='莫得感情')
#
#         # 删除：
#         # 单条删除：
#         # Projects.objects.get(id=5).delete()
#         # 批量删除：
#         # Projects.objects.filter(name__contains='2').delete()
#
#         # 单表写聚合函数：
#         # 直接调用aggregate函数，传入聚合函数，参数传要计算的字段值（并非分组查询）
#         qs = Projects.objects.filter(name__contains='项目').aggregate(Count('id'))
#
#         # 多表分组查询：
#         # 前面写主表字段，聚合函数里接子表模型类名小写
#         # qs = Projects.objects.values('id').annotate(Count('interfaces'))
#         pass


class InterfacesView(View):
    def get(self, request):
        queryset = Interfaces.objects.all()
        res_ser = InterfacesSerializer(instance=queryset, many=True)
        return JsonResponse(res_ser.data, safe=False)


class InterfacesDetailView(View):
    def get(self, request, pk):
        obj = Interfaces.objects.get(id=pk)
        res_ser = InterfacesSerializer(instance=obj)
        return JsonResponse(res_ser.data, safe=False)