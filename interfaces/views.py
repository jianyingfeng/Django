from django.shortcuts import render
from .models import Interfaces
from projects.models import Projects
from django.http import HttpResponse
from django.views import View
from django.db import connection


class InterfacesView(View):
    def get(self, request, pk):
        # 创建从表数据，外键如何传值？
        # 方式一：
        # 1）获取父表模型对象
        # 2）从表外键字段传参为父表模型对象
        # projects_obj = Projects.objects.get(name='在线图书项目')
        # interfaces_obj = Interfaces.objects.create(name='在线图书项目-注册接口',tester='李莫愁',projects=projects_obj)
        # 方式二：
        # 1）获取父表模型对象，再获取模型对象的id
        # 2）从表外键字段_id，传参为父表模型对象的id
        # projects_obj = Projects.objects.get(name='在线图书项目')
        # interfaces_obj = Interfaces.objects.create(name='在线图书项目-订单接口', tester='李莫愁', projects_id=projects_obj.id)
        # 查询接口名称包含‘登录’的项目数据
        # 1）先按条件取到接口表数据，再通过外键属性查询父表数据
        # Interfaces.objects.filter(name__contains='登录').first().projects
        # 查询项目负责人包含‘热水’的接口数据
        # 方式一：从子表查到父表
        # Interfaces.objects.filter(projects__leader__contains='热水')
        # 方式二：
        # 从父表查到字表
        # Projects.objects.filter(leader__contains='热水').first().interfaces_set.all()
        pass

    def post(self, request, pk):
        return HttpResponse('<h1>新增项目信息</h1>')

    def put(self, request):
        return HttpResponse('<h1>修改项目信息</h1>')

    def delete(self, request):
        return HttpResponse('<h1>删除项目信息</h1>')
