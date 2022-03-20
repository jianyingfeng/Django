from rest_framework import routers
from testsuites.views import TestsuitesViewSet

routers =routers.SimpleRouter()
routers.register(r'testsuits', TestsuitesViewSet)

urlpatterns = []
urlpatterns += routers.urls