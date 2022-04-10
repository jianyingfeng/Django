from rest_framework import routers
from reports.views import ReportViewSet

routers = routers.SimpleRouter()
routers.register(r'reports', ReportViewSet)

urlpatterns = []
urlpatterns += routers.urls
