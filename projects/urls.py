from django.urls import path, include
from rest_framework import routers

from projects import views

# 1、可以使用路由对象，为视图集类（重点）自动生成路由条目
# 2、只会给通用的action函数生成路由条目，不会给自定义的生成
# 3、创建SimpleRouter路由对象
# DefaultRouter与SimpleRouter类似，不过DefaultRouter会在访问“/”路由时提供一个子应用根路由
router = routers.SimpleRouter()
# router = routers.DefaultRouter()
# 4、register方法进行注册
# 5、prefix指定路由前缀
# 6、viewset指定视图集，不能调用as_view方法
router.register(r'projects', views.ProjectsViewSet)

urlpatterns = [
    # path('create/', views.create_project),
    # path('put/', views.put_project),
    # path('get/', views.get_project),
    # path('delete/', views.delete_project),
    # path('projects/', views.ProjectsView.as_view()),
    # path('projects/<int:pk>/', views.ProjectsDetailView.as_view()),
    # path('projects/', views.ProjectsViewSet.as_view({
    #     'get': 'list',
    #     'post': 'create'
    # })),
    # path('projects/<int:pk>/', views.ProjectsViewSet.as_view({
    #     'get': 'retrieve',
    #     'put': 'update',
    #     'patch': 'partial_update',
    #     'delete': 'destroy'
    # })),
    # path('projects/names/', views.ProjectsViewSet.as_view({
    #     'get': 'names',
    # })),
    # path('projects/<int:pk>/interfaces/', views.ProjectsViewSet.as_view({
    #     'get': 'interfaces',
    # })),
    # 7、加载路由条目
    # 方式一：urls属性可获取生成的路由条目
    path('', include(router.urls)),
]
# 方式二：
# router.urls为列表
# urlpatterns += router.urls
