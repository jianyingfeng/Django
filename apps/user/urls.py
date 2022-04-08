from django.urls import path, re_path
from user import views


urlpatterns = [
    path('user/register/', views.RegisterUserViewSet.as_view(
        {
            'post': 'create'
        }
    )),
    # 匹配用户名的正则表达式
    re_path(r'^user/(?P<username>\w{6,20})/count/$', views.RegisterUserViewSet.as_view(
        {
            'get': 'count_username'
        },
    )),
    # 匹配邮箱的正则表达式
    re_path(r'^user/(?P<email>[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+))/count/$',
            views.RegisterUserViewSet.as_view(
        {
            'get': 'count_email'
        },
    ))
]


# from django.urls import path, include
# from rest_framework import routers
#
# from user import views
#
#
# router = routers.SimpleRouter()
#
# router.register(r'user', views.RegisterUserViewSet)
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]