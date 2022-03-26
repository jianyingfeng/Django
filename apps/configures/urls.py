from rest_framework import routers
from configures.views import ConfigViewSet

routers = routers.SimpleRouter()
routers.register(r'configures', ConfigViewSet)

urlpatterns = []
urlpatterns += routers.urls