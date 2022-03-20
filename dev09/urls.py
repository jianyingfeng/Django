"""dev09 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
# from apps.projects import views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

SchemaView = get_schema_view(
    openapi.Info(
        title="lemon API接口文档平台",  # 必传
        default_version='v1',  # 必传
        description="这是一个美轮美奂的接口文档",
        contact=openapi.Contact(email="1055193533@qq.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    # schema view本身的权限类
    # permission_classes=(permissions.AllowAny,),  # 权限类
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 如果全局路由和子路由相同，且指向了不同的视图函数，那么谁先被匹配到，就调用谁的视图函数（即谁写在上面谁优先）
    # path('project/index/', views.index),
    # path('project/', include('projects.urls')),
    # path('project/<int:pk>',views.get_project_by_id),
    path('', include('projects.urls')),
    path('', include('interfaces.urls')),
    path('', include('envs.urls')),
    path('', include('debugtalks.urls')),
    path('', include('testsuites.urls')),
    path('', include('reports.urls')),
    path('', include('testcases.urls')),
    path('', include('user.urls')),
    # 指定测试平台接口文档的url
    path('docs/', include_docs_urls(title='测试平台接口文档', description='xxx接口文档')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),  # 导出
    path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # redoc美化UI
    path('redoc/', SchemaView.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
    # 在全局路由表中添加rest_framework.urls路由
    # rest_framework.urls提供了登入和登出的功能
    path('api/', include('rest_framework.urls')),
    # 提供token认证
    path('user/login/', obtain_jwt_token)
]