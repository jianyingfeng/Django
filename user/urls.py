from django.urls import path, re_path, include
from user import views


urlpatterns = [
    path('user/register/', views.RegisterUserViewSet.as_view(
        {
            'post': 'create'
        }
    )),
    re_path(r'^user/(?P<username>\w{6,20})/count/$', views.RegisterUserViewSet.as_view(
        {
            'get':'count_username'
        }
    ))
    # re_path(r'user/(.+?)/count_username/', views.RegisterUserViewSet.as_view(
    #     {
    #         'get':'count_username'
    #     }
    # ))
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