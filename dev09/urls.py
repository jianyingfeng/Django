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
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from projects import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # 如果全局路由和子路由相同，且指向了不同的视图函数，那么谁先被匹配到，就调用谁的视图函数（即谁写在上面谁优先）
    # path('project/index/', views.index),
    # path('project/', include('projects.urls')),
    # path('project/<int:pk>',views.get_project_by_id),
    path('', include('projects.urls')),
    path('', include('interfaces.urls')),
    # 指定测试平台接口文档的url
    path('docs/', include_docs_urls(title='测试平台接口文档', description='xxx接口文档'))
]