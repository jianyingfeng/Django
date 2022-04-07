from rest_framework import routers

from envs import views

routers = routers.SimpleRouter()
routers.register(r'envs', views.EnvsViewSet)

urlpatterns = []
urlpatterns += routers.urls
