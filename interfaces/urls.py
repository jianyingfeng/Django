from django.urls import path
from interfaces import views


urlpatterns = [
    # path('create/', views.create_project),
    # path('put/', views.put_project),
    # path('get/', views.get_project),
    # path('delete/', views.delete_project),
    path('interfaces/<int:pk>/',views.InterfacesView.as_view())
]