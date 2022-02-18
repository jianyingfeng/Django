from django.urls import path, include
from user import views

urlpatterns = [
    path('user/register/', views.RegisterUserView.as_view()),
]