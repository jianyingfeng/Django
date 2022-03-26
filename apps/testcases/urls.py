from rest_framework import routers
from testcases.views import TestcasesViewSet

routers = routers.SimpleRouter()
routers.register(r'testcases', TestcasesViewSet)

urlpatterns = []
urlpatterns += routers.urls
