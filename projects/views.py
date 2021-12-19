from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View
import json

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
        projects_data = {
            'id':pk,
            'name':'xxx项目',
            'leader':'潘潘达'
        }
        projects_data_list = [
            {
                'id': 1,
                'name': 'xxx项目',
                'leader': '潘潘达'
            },
            {
                'id': 2,
                'name': 'yyy项目',
                'leader': '多喝热水'
            },
            {
                'id': 3,
                'name': 'zzz项目',
                'leader': '醉了'
            }
        ]
        # res_str = json.dumps(projects_data, ensure_ascii=False)
        # return HttpResponse(res_str,content_type='application/json',status:201)
        # return HttpResponse(f'<h1>获取项目{pk}的信息</h1>')
        return JsonResponse(projects_data_list, json_dumps_params={'ensure_ascii':False}, safe=False)

    def post(self, request, pk):
        return HttpResponse('<h1>新增项目信息</h1>')

    def put(self, request):
        return HttpResponse('<h1>修改项目信息</h1>')

    def delete(self, request):
        return HttpResponse('<h1>删除项目信息</h1>')