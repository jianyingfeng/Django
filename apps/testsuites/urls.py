from rest_framework import routers
from testsuites.views import TestsuiteViewSet

routers = routers.SimpleRouter()
routers.register(r'testsuits', TestsuiteViewSet)

urlpatterns = []
urlpatterns += routers.urls
