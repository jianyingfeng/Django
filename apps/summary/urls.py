from rest_framework.urls import path

from summary import views


urlpatterns = [
    path('summary/', views.SummaryView.as_view())
]
