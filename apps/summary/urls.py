from rest_framework.urls import path

from summary import views


urlpatterns = [
    path('summary/', views.SummaryViewSet.as_view(
        {
            'get': 'get_summary'
        }
    ))
]
# urlpatterns += routers.urls
