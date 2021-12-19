from django.urls import path
from projects import views


urlpatterns = [
    # path('create/', views.create_project),
    # path('put/', views.put_project),
    # path('get/', views.get_project),
    # path('delete/', views.delete_project),
    path('projects/<int:pk>/',views.ProjectsView.as_view())
]