from rest_framework import routers
from debugtalks.views import DebugtalkViewSet

routers = routers.SimpleRouter()
routers.register(r'debugtalks', DebugtalkViewSet)

urlpatterns = []
urlpatterns += routers.urls