from django.urls import path
from task_manager.statuses import views

app_name = 'statuses'

urlpatterns = [
    path('', views.StatusesView.as_view(), name="show_statuses"),
    path('create/', views.StatusCreateView.as_view(), name="create_status"),
    path('<int:pk>/update/', views.StatusUpdateView.as_view(), name="edit_status"),
    path('<int:pk>/delete/', views.StatusDeleteView.as_view(), name="delete_status"),
]
